<script>
  /** @type {import('./$types').PageData} */
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import { browser } from "$app/environment";

  export let data;
  let email = "";
  let password = "";

  let text = "";

  let loading = false;

  let token = "";

  onMount(async () => {
    token = localStorage.getItem("token") || "";
    if (token != "") {
      window.location.replace("/feed");
    }
  });

  async function login() {
    loading = true;
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `password=${password}&email=${email}`,
    });

    if (!response.error) {
      const responseData = await response.json();
      loading = false;
      if (responseData.error) {
        text = responseData.error;
        resp.showModal();
      }
      if (responseData.token) {
        token = responseData.token;
        localStorage.setItem("token", token);
        if (token != "") {
          window.location.replace("/feed");
        }
      }
    } else {
      // Request failed, handle the error
      console.error("Request failed");
    }
  }
</script>

<div class="hero min-h-screen bg-base-200">
  <div class="hero-content flex-col lg:flex-row-reverse">
    <div class="text-center lg:text-left">
      <h1 class="text-5xl font-bold">
        M<span class="text-primary">ask</span>IT
      </h1>
      <p class="py-6">
        Discover the Unseen, Say the Unspoken. Anonymously Yours, MaskIT​
      </p>
    </div>
    <div>
      <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
        <form class="card-body">
          <div class="form-control">
            <label class="label">
              <span class="label-text">Student email</span>
            </label>
            <input
              bind:value={email}
              type="email"
              placeholder="XXX@learner.manipal.edu"
              class="input input-bordered"
              required
            />
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text">Password</span>
            </label>
            <input
              bind:value={password}
              type="password"
              placeholder="password"
              class="input input-bordered"
              required
            />
            <label class="label">
              <a href="#" class="label-text-alt link link-hover"
                >Forgot password?</a
              >
            </label>
          </div>
          <div class="form-control mt-6">
            <button class="btn btn-primary" on:click={login}
              >{#if !loading}Login{:else}<span
                  class="loading loading-infinity loading-lg"
                ></span>{/if}</button
            >
          </div>
        </form>
      </div>
      <div class="card bg-base-100 shadow-xl m-3">
        <div class="card-body">
          <p>
            Don't have an account? <a class="link link-info" href="/signup">
              Sign Up</a
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</div>

<dialog id="resp" class="modal">
  <div class="modal-box w-11/12 max-w-5xl">
    <h3 class="font-bold text-lg">MaskIT</h3>
    <p class="py-4">{text}</p>
    <div class="modal-action">
      <form method="dialog">
        <!-- if there is a button, it will close the modal -->
        <button class="btn btn-primary">Close</button>
      </form>
    </div>
  </div>
</dialog>
