package main

import (
	"log"
	"database/database.go"
	"routes"

	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	database.InitMongoDB()

	app.Post("/api/posts", routes.CreatePost)
	app.Get("/api/posts/:id", routes.GetPostsByUser)
	app.Get("/api/allposts", routes.GetAllPosts)

	log.Fatal(app.Listen(":5001"))
}
