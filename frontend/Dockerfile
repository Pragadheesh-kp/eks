# Use an official Nginx image as the base image
FROM nginx:alpine

# Copy the frontend.html to the default Nginx HTML directory
COPY frontend.html /usr/share/nginx/html/index.html

# Expose port 80 for the application
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
