CREATE TABLE books (
	id UUID DEFAULT uuid_generate_v4 () PRIMARY KEY,
	"url" VARCHAR(255) NOT NULL,
	"title" VARCHAR(255) NOT NULL,
	"category" VARCHAR(100) NOT NULL,
	"price" NUMERIC(7,2) NOT NULL,
	"reviews" INTEGER NOT NULL
);