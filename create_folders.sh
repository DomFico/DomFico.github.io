#!/bin/bash

# Create directories
mkdir -p "Coding Projects"
mkdir -p "Research"

# Create test.txt files in each directory
echo "This is a test file in Coding Projects." > "Coding Projects/test.txt"
echo "This is a test file in Research." > "Research/test.txt"

echo "Directories and test files have been created."