<template>
  <div class="container">

    <!-- 🔐 AUTH SECTION -->
    <div v-if="!token" class="auth-box">

      <h2>{{ isLogin ? "🔐 Login" : "📝 Register" }}</h2>

      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />

      <button @click="handleAuth">
        {{ isLogin ? "Login" : "Register" }}
      </button>

      <p class="switch" @click="isLogin = !isLogin">
        {{ isLogin ? "Create account" : "Already have account? Login" }}
      </p>

      <p v-if="message" class="message">{{ message }}</p>

    </div>

    <!-- 🧠 TASKS SECTION -->
    <div v-else>

      <h2>📝 Task Weather Manager</h2>

      <button class="logout" @click="logout">Logout</button>

      <p v-if="message" class="message">
        {{ message }}
      </p>

      <!-- FORM -->
      <div class="form">
        <input v-model="title" placeholder="Task title" />
        <input v-model="city" placeholder="City" />
        <button @click="addTask">Add Task</button>
      </div>

      <!-- TASK LIST -->
      <div v-for="task in tasks" :key="task.id" class="task">
        <h3>{{ task.title }}</h3>
        <p>📍 {{ task.city }}</p>
        <p>🌤 {{ task.weather }}</p>

        <button class="delete" @click="deleteTask(task.id)">
          🗑
        </button>
      </div>

    </div>

  </div>
</template>

<script>
import API from "./api";

export default {
  data() {
    return {
      // auth
      username: "",
      password: "",
      isLogin: true,
      token: localStorage.getItem("token"),

      // tasks
      title: "",
      city: "",
      tasks: [],

      message: ""
    };
  },

  methods: {

      validateAuth() {
  if (!this.username || !this.password) {
    this.message = "❌ Username and password are required";
    return false;
  }

  if (this.password.length < 6) {
    this.message = "❌ Password must be at least 6 characters";
    return false;
  }

  return true;
},
    // ================= AUTH =================
    async handleAuth() {

      // ✅ validation avant appel API
      if (!this.validateAuth()) return;

      try {

        if (this.isLogin) {
          const res = await API.post("/login", {
            username: this.username,
            password: this.password
          });

          this.token = res.data.access_token;
          localStorage.setItem("token", this.token);

          this.message = "✅ Login successful";

          this.loadTasks();

        } else {
          await API.post("/register", {
            username: this.username,
            password: this.password
          });

          this.message = "✅ User created, now login";
          this.isLogin = true;
        }

      } catch (err) {
        this.message = "❌ " + (err.response?.data?.detail || "Auth error");
      }
    },

    logout() {
      localStorage.removeItem("token");
      this.token = null;
      this.tasks = [];
    },

    // ================= TASKS =================
    async loadTasks() {
      try {
        const res = await API.get("/tasks");
        this.tasks = res.data;
      } catch (error) {
        this.message = "❌ Failed to load tasks";
      }
    },

    async addTask() {
      if (!this.title || !this.city) return;

      try {
        await API.post("/tasks", {
          title: this.title,
          city: this.city
        });

        this.title = "";
        this.city = "";

        this.message = "✅ Task added successfully";

        this.loadTasks();

        setTimeout(() => this.message = "", 2000);

      } catch (error) {
        this.message = "❌ Failed to add task";
      }
    },

    async deleteTask(id) {
      try {
        await API.delete(`/tasks/${id}`);

        this.message = "🗑 Task deleted";

        this.loadTasks();

        setTimeout(() => this.message = "", 1500);

      } catch (error) {
        this.message = "❌ Delete failed";
      }
    }
  },

  mounted() {
    if (this.token) {
      this.loadTasks();
    }
  }
};
</script>

<style>
.container {
  max-width: 600px;
  margin: auto;
  font-family: Arial;
}

/* AUTH */
.auth-box {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 80px;
}

input {
  padding: 8px;
  width: 100%;
}

button {
  padding: 8px;
  background: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

.logout {
  background: black;
  margin-bottom: 10px;
}

.task {
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
}

.delete {
  background: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.switch {
  color: blue;
  cursor: pointer;
}

.message {
  padding: 10px;
  background: #f5f5f5;
  margin: 10px 0;
}
</style>