// TODO: compute stats + bucket URLs per hostname
// On the complexity of Go timeouts : https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
package main

import (
    "bufio"
    "crypto/tls"
    "fmt"
    "log"
    "net/http"
    "os"
    "time"
)

type CrawlResult struct {
    url      string
    status   int
    err      error
    duration Duration
}

func main() {
    var urls []string
    lineReader := bufio.NewScanner(os.Stdin)
    for lineReader.Scan() {
        urls = append(urls, lineReader.Text())
    }
    tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }
    client := &http.Client{Transport: tr, Timeout: 120 * time.Second} // there is no timeout by default
    channel := make(chan *CrawlResult /*buffer_size=*/, 100)
    durations := make([]Duration, len(urls))
    for _, url := range urls {
        go func(url string) {
            start := time.Now()
            resp, err := client.Get(url)
            var result *CrawlResult
            if resp == nil {
                result = &CrawlResult{url, 0, err, time.Now().Sub(start)}
            } else {
                resp.Body.Close()
                result = &CrawlResult{url, resp.StatusCode, err, time.Now().Sub(start)}
            }
            for { // as long as the channel is full, we retry
                select {
                case channel <- result:
                    return
                }
            }
        }(url)
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
                return
            }
        }
    }
}
