// On the complexity of Go timeouts : https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
package main

import (
    "bufio"
    "crypto/tls"
    "fmt"
    "html"
    "log"
    "math/rand"
    "net/http"
    "net/url"
    "os"
    "sort"
    "time"
)

type CrawlResult struct {
    url      string
    status   int
    err      error
    duration time.Duration
}

func shuffle(array []string) {
    for i := len(array) - 1; i > 0; i-- {
        j := rand.Intn(i + 1)
        array[i], array[j] = array[j], array[i]
    }
}

type ByLength []time.Duration

func (a ByLength) Len() int           { return len(a) }
func (a ByLength) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByLength) Less(i, j int) bool { return a[i].Seconds() < a[j].Seconds() }

func displayTimingStats(durations []time.Duration) {
    sort.Sort(ByLength(durations))
    total := Sum(durations)
    log.Println("count:", len(durations))
    log.Println("mean:", total/float64(len(durations)))
    log.Println("p00_min:", durations[0])
    log.Println("p01:", percentile(durations, .01))
    log.Println("p10:", percentile(durations, .1))
    log.Println("p50_median:", percentile(durations, .5))
    log.Println("p90:", percentile(durations, .9))
    log.Println("p99:", percentile(durations, .99))
    log.Println("p100:", percentile(durations, .99))
    log.Println("p100_max:", durations[len(durations)-1])
    log.Println("sum:", total)
}

func Sum(durations []time.Duration) float64 {
    sum := 0.0
    for _, duration := range durations {
        sum += duration.Seconds()
    }
    return sum
}

func percentile(durations []time.Duration, percent float64) float64 {
    index := float64(len(durations)-1) * percent
    return durations[int(index)].Seconds()
}

func bucketUrlsPerHostname(urls []string) map[string][]string {
    urlsPerHostnames := make(map[string][]string)
    for _, hostUrl := range urls {
        parsedUrl, _ := url.Parse(hostUrl)
        hostname := parsedUrl.Host
        if hostUrls, exist := urlsPerHostnames[hostname]; exist {
            urlsPerHostnames[hostname] = append(hostUrls, hostUrl)
        } else {
            urlsPerHostnames[hostname] = []string{hostUrl}
        }
    }
    return urlsPerHostnames
}

func main() {
    var urls []string
    lineReader := bufio.NewScanner(os.Stdin)
    for lineReader.Scan() {
        urls = append(urls, html.UnescapeString(lineReader.Text()))
    }
    shuffle(urls)
    urlsPerHostnames := bucketUrlsPerHostname(urls)
    tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }
    client := &http.Client{Transport: tr, Timeout: 120 * time.Second} // there is no timeout by default
    channel := make(chan *CrawlResult /*buffer_size=*/, 100)
    durations := make([]time.Duration, len(urls))
    for _, urls := range urlsPerHostnames {
        go func(urls []string) {
            for i, url := range urls {
                if i > 0 {
                    time.Sleep(2)
                }
                start := time.Now()
                resp, err := client.Get(url)
                var result *CrawlResult
                if resp == nil {
                    result = &CrawlResult{url, 0, err, time.Now().Sub(start)}
                } else {
                    resp.Body.Close()
                    result = &CrawlResult{url, resp.StatusCode, err, time.Now().Sub(start)}
                }
            loop:
                for { // as long as the channel is full, we retry
                    select {
                    case channel <- result:
                        break loop
                    }
                }
            }
        }(urls)
    }
    count := 0
    for {
        select {
        case result := <-channel:
            if result.err != nil {
                fmt.Println(result.err, result.url)
            } else if result.status != 200 {
                fmt.Println(result.status, result.url)
            }
            durations[count] = result.duration
            count += 1
            log.Println(count, result.url, result.status)
            if count == len(urls) {
                displayTimingStats(durations)
                return
            }
        }
    }
}
