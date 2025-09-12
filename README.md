# 🗳️ Online Poll System Backend

## 📌 Overview
This project is part of **Project Nexus**, the capstone stage of the **ProDev Backend Engineering Program**.  
It demonstrates the ability to design, build, and document a **real-world backend system** using **industry best practices**.

The **Online Poll System Backend** simulates applications requiring **real-time data processing**.  
It provides APIs for:
- ✅ Creating and managing polls  
- ✅ Casting votes securely  
- ✅ Fetching real-time results  

The project emphasizes **scalable database design, secure APIs, and professional documentation**.

---

## 🎯 Project Goals
- **API Development** → Endpoints for polls, votes, and results.  
- **Database Efficiency** → Optimized schemas for real-time results.  
- **Documentation** → Swagger API docs at `/api/docs`.  
- **Professional Workflow** → Version control, clean commits, CI/CD.  

---

## 🛠️ Tech Stack
- **Django** – High-level Python backend framework  
- **PostgreSQL** – Relational database  
- **Django REST Framework (DRF)** – RESTful APIs  
- **Swagger / OpenAPI** – Interactive API docs  
- **Docker** – Deployment & containerization  
- **Redis & Celery (future)** – Background tasks & caching  

---

## ✨ Features
1. **Poll Management**  
   - Create polls with multiple options  
   - Metadata: creation date, expiry date  

2. **Voting System**  
   - Secure endpoints for votes  
   - Duplicate vote prevention  
   - Input validation  

3. **Result Computation**  
   - Real-time vote counts  
   - Optimized queries for scalability  

4. **API Documentation**  
   - Swagger UI available at `/api/docs`  

---

## 🚀 Setup & Installation
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/online-poll-system-backend.git
cd online-poll-system-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
````

### API Docs

Visit [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs) for Swagger documentation.

---

## 📂 Repository Structure

```
online-poll-system-backend/
│── polls/                # Poll app (models, views, serializers, urls)
│── project_nexus/        # Project settings & configs
│── requirements.txt      # Dependencies
│── README.md             # Documentation
│── manage.py             # Django management script
```

---

## 📊 Evaluation Criteria

* ✅ **Functionality** – Poll creation, voting, results work flawlessly
* ✅ **Code Quality** – Clean, modular, best practices
* ✅ **Database Design** – Efficient, normalized schema
* ✅ **Performance** – Handles high-frequency voting
* ✅ **Documentation** – Clear README & Swagger UI

---

## 📍 Project Links

* **GitHub Repo:** \[🔗 Add Link Here]
* **ERD Diagram:** \[🔗 Add Link Here]
* **Slides (Google Slides):** \[🔗 Add Link Here]
* **Demo Video (≤5 mins):** \[🔗 Add Link Here]

---

## 🤝 Contribution

1. Fork the repository
2. Create a feature branch → `git checkout -b feature/your-feature`
3. Commit changes → `git commit -m "feat: add your feature"`
4. Push to branch → `git push origin feature/your-feature`
5. Open a Pull Request

---

## 🌱 Next Steps

* Add **JWT Authentication** for secure sessions
* Implement **Redis caching** for results
* Explore **GraphQL API** alternative
* Deploy with **CI/CD pipelines**

---

## 📜 References

* [Django Docs](https://docs.djangoproject.com/)
* [PostgreSQL Docs](https://www.postgresql.org/docs/)
* [DRF Docs](https://www.django-rest-framework.org/)
* [Swagger Docs](https://swagger.io/specification/)
* [Docker Docs](https://docs.docker.com/)
* [Celery Docs](https://docs.celeryq.dev/)

---

🔥 This project reflects my **backend engineering expertise** and serves as a **portfolio-ready, real-world application**.

``` 
