package main

import (
	"context"
	"crypto/tls"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

type healthCheckServer struct {
	grpc_health_v1.UnimplementedHealthServer
}

func (s *healthCheckServer) Check(ctx context.Context, in *grpc_health_v1.HealthCheckRequest) (*grpc_health_v1.HealthCheckResponse, error) {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Errorf(codes.DataLoss, "failed to get metadata")
	}
	v := md.Get("want-health-check-response")
	if len(v) != 1 {
		return &grpc_health_v1.HealthCheckResponse{
			Status: grpc_health_v1.HealthCheckResponse_UNKNOWN,
		}, nil
	}
	return &grpc_health_v1.HealthCheckResponse{
		Status: grpc_health_v1.HealthCheckResponse_ServingStatus(grpc_health_v1.HealthCheckResponse_ServingStatus_value[v[0]]),
	}, nil
}

func main() {
	ctx, cancel := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGINT, syscall.SIGTERM)
	defer cancel()
	port := 50051
	useTLS := false
	if i, err := strconv.Atoi(os.Getenv("PORT")); err == nil {
		port = i
	}
	if b, err := strconv.ParseBool(os.Getenv("USE_TLS")); err == nil {
		useTLS = b
	}
	var s *grpc.Server
	if useTLS {
		serverCert, err := tls.LoadX509KeyPair("server.pem", "server-key.pem")
		if err != nil {
			log.Fatalln(err)
		}
		s = grpc.NewServer(
			grpc.Creds(credentials.NewTLS(&tls.Config{
				Certificates: []tls.Certificate{serverCert},
				ClientAuth:   tls.NoClientCert,
			})),
		)
	} else {
		s = grpc.NewServer()
	}
	grpc_health_v1.RegisterHealthServer(s, &healthCheckServer{})

	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Println("gRPC server is serving")
	go s.Serve(lis)
	<-ctx.Done()
	log.Println("gRPC server is graceful stopping")
	s.GracefulStop()
}
