//go:build ignore
// +build ignore

package main

import (
	"log"
	"net/http"
	_ "net/http/pprof"
)

func main() {
	log.Fatal(http.ListenAndServe(":8888", nil))
}
