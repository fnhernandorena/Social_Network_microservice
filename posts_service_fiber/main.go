package main

import (
	"log"
	"posts_service_fiber/database"
	"posts_service_fiber/routes"

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
