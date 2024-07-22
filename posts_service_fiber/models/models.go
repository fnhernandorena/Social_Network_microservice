package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Post struct {
	ID      primitive.ObjectID `json:"id,omitempty" bson:"_id,omitempty"`
	UserID  string             `json:"user_id" bson:"user_id"`
	Title   string             `json:"title" bson:"title"`
	Content string             `json:"content" bson:"content"`
}

type User struct {
	ID       string `json:"_id,omitempty" bson:"_id,omitempty"`
	Username string `json:"username,omitempty"`
	Age      int    `json:"age,omitempty"`
}

type PostWithUser struct {
	Post
	Username string `json:"username"`
	Age      int    `json:"age"`
}
