<template>
  <div class="auth-container">

    <h2>{{ isLogin ? "🔐 Login" : "📝 Register" }}</h2>

    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />

    <button @click="handleSubmit">
      {{ isLogin ? "Login" : "Register" }}
    </button>

    <p class="switch" @click="isLogin = !isLogin">
      {{ isLogin ? "Create account" : "Already have account? Login" }}
    </p>

    <p v-if="message" class="msg">{{ message }}</p>

  </div>
</template>

<script>
import API from "../api";

export default {
  data() {
    return {
      username: "",
      password: "",
      isLogin: true,
      message: ""
    };
  },

  methods: {
    async handleSubmit() {
      try {
        if (this.isLogin) {
          const res = await API.post("/login", {
            username: this.username,
            password: this.password
          });

          localStorage.setItem("token", res.data.access_token);

          this.message = "✅ Login successful";

          // redirect
          setTimeout(() => {
            window.location.href = "/";
          }, 1000);

        } else {
          await API.post("/register", {
            username: this.username,
            password: this.password
          });

          this.message = "✅ Account created! Switch to login";
          this.isLogin = true;
        }

      } catch (err) {
        this.message = "❌ Error: " + (err.response?.data?.detail || "Server error");
      }
    }
  }
};
</script>

<style>
.auth-container {
  width: 300px;
  margin: 100px auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-family: Arial;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
}

button {
  padding: 10px;
  background: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

.switch {
  color: blue;
  cursor: pointer;
  font-size: 12px;
}

.msg {
  margin-top: 10px;
  font-weight: bold;
}
</style>