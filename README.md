# Workout Logging API

A FastAPI + Supabase backend for logging workouts.

## Features
- POST /workouts: create workout entry
- GET /workouts/results-by-date: date-range query
- GET /workouts/results?days=:RESULT: sliding window query

## Tech
- FastAPI
- Supabase (PostgreSQL)
- Pydantic models
