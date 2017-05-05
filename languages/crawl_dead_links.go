//usr/bin/env go run "$0" "$@"; exit "$?"
// TODO: install go 1.8
// On the complexity of Go timeouts : https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
package main

import (
    "bufio"
    "crypto/tls"
    "fmt"
    //"log"
    "net/http"
    "os"
    "time"
)

type CrawlResult struct {
    url        string
    statusCode int
    err        error
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
    client := &http.Client{Transport: tr, Timeout: 15 * time.Second}
    channel := make(chan *CrawlResult, len(urls))
    for _, url := range urls {
        go func(url string) {
            resp, err := client.Get(url)
            if err != nil && resp != nil {
                resp.Body.Close()
            }
            if resp == nil {
                channel <- &CrawlResult{url, 0, err}
            } else {
                channel <- &CrawlResult{url, resp.StatusCode, err}
            }
        }(url)
    }
    for {
        select {
        case result := <-channel:
            if result.err != nil {
                fmt.Println(result.err.Error(), result.url)
            } else if result.statusCode != 200 {
                fmt.Println(result.statusCode, result.url)
            }
        }
    }
}
