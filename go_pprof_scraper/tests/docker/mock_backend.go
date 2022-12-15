//go:build ignore
// +build ignore

package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
	"sync/atomic"
	"time"
)

var accepted int64

func main() {
	http.HandleFunc("/accepted", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "%d", atomic.LoadInt64(&accepted))
	})
	http.HandleFunc("/profiles", handler)
	log.Fatal(http.ListenAndServe(":9999", nil))
}

func handler(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseMultipartForm(-1); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintf(w, "failed to parse form: %s\n", err)
		return
	}

	if v := r.Form.Get("family"); v != "go" {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintf(w, "bad family, wanted go, got %s\n", v)
		return
	}
	if v := r.Form.Get("version"); v != "3" {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintf(w, "bad version, wanted 3, got %s\n", v)
		return
	}

	for _, form := range []string{"start", "end"} {
		v := r.Form.Get(form)
		if v == "" {
			w.WriteHeader(http.StatusBadRequest)
			fmt.Fprintf(w, "missing required form field \"%s\"\n", form)
			return
		}
		if _, err := time.Parse(time.RFC3339, v); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			fmt.Fprintf(w, "%s time must be in RFC3339 (ISO 8601) format: %s\n", form, err)
			return
		}
	}

	expected := []string{
		"foo:bar",
		"runtime:go",
		"service:testing",
	}
	tags := r.Form["tags[]"]
	for _, v := range expected {
		if !contains(tags, v) {
			w.WriteHeader(http.StatusBadRequest)
			fmt.Fprintf(w, "missing expected tag %s\n", v)
			return
		}
	}

	// expectedPrefixes are tags where they should be sent, but we don't
	// want to overfit on the exact value
	expectedPrefixes := []string{
		"runtime-id:",
		"profiler_version:",
	}
	for _, v := range expectedPrefixes {
		if !containsPrefix(tags, v) {
			w.WriteHeader(http.StatusBadRequest)
			fmt.Fprintf(w, "missing expected tag %s\n", v)
			return
		}
	}

	if _, ok := r.MultipartForm.File["data[heap.pprof]"]; !ok {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintf(w, "missing data[heap.pprof], have values %v\n", r.MultipartForm.File)
		return
	}
	// All good, consider this accepted
	atomic.AddInt64(&accepted, 1)
}

func contains(vals []string, s string) bool {
	for _, v := range vals {
		if v == s {
			return true
		}
	}
	return false
}

func containsPrefix(vals []string, s string) bool {
	for _, v := range vals {
		if strings.HasPrefix(v, s) {
			return true
		}
	}
	return false
}
