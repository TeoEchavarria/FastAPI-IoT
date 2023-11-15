# FastAPI-IoT
FastAPI-IoT is a project focused on building a robust API for managing Internet of Things (IoT) devices and users. It includes user CRUD operations, CRUD operations for things (devices), and an API with MySQL database connectivity. Additionally, it offers visualization, monitoring, and control of processes (coming soon).

## MySQL - Database Structure
<p align="center">
  <img src="https://user-images.githubusercontent.com/63327224/154146336-1e270c8b-ad39-4efc-9d98-754f3d6c7e64.jpg" width="350">
  <img src="https://user-images.githubusercontent.com/63327224/154146638-07736fbb-5339-40c8-baa7-5d9fdc80ee1a.jpg" width="350">
</p>

## Clarifications
- In the Things table, the column modification_dates is a set of all the dates on which a Thing has been used.
- In the Users table, the column things is a set of all UUIDs that reference the Things available to a user.
- In Development

We are currently working on creating an additional database to store the data collected by each Thing. This data will be analyzed and the analysis results will also be stored for comparison and temporal tracking of results. The analysis will be performed using specialized Python libraries, utilizing methods such as Maximum Likelihood for probability analysis in stochastic processes. Stay tuned for updates!

Feel free to customize and expand this README to provide more details about your project, installation instructions, and any other relevant information.
