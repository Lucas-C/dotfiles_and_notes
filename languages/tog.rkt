#lang typed/racket
;; Using higher-order occurrence typing
(define-type SrN (U String Number))
(: tog ((Listof SrN) -> String))
(define (tog l)
   (apply string-append (filter string? l)))
(tog (list 5 "hello " 1/2 "world" (sqrt -1)))
;; Racket's type system is designed to let you add types after you've worked for
;; a while in untyped mode — even if your untyped program wouldn't fit nicely
;; in a conventional type system.
