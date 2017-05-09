extern crate curl;
extern crate futures;
extern crate tokio_core;
extern crate tokio_curl;

use std::io::{self, Write};

use curl::easy::Easy;
use futures::Future;
use tokio_core::reactor::Core;
use tokio_curl::Session;

fn main() {
    // Create an event loop that we'll run on, as well as an HTTP `Session`
    // which we'll be routing all requests through.
    let mut lp = Core::new().unwrap();
    let session = Session::new(lp.handle());

    // Prepare the HTTP request to be sent.
    let mut req = Easy::new();
    req.get(true).unwrap();
    req.url("https://www.rust-lang.org").unwrap();
    req.write_function(|data| {
        io::stdout().write_all(data).unwrap();
        Ok(data.len())
    }).unwrap();

    // Once we've got our session, issue an HTTP request to download the
    // rust-lang home page
    let request = session.perform(req);

    // Execute the request, and print the response code as well as the error
    // that happened (if any).
    let mut req = lp.run(request).unwrap();
    println!("{:?}", req.response_code());
}