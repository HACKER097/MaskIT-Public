<script>
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { jwtDecode } from "jwt-decode";

function myProfile(){
    let id = jwtDecode(localStorage.getItem("token"))["sub"];
    window.location.replace(`/profile/${id}`);
  }

  function logout(){
    localStorage.setItem("token", "");
    window.location.replace(`/login`);
  }
</script>

<div class="navbar bg-base-100 shadow-xl">
  <div class="flex-1">
    <a class="btn btn-ghost text-3xl" href="/feed">MaskIT​</a>
  </div>
  <button class="btn btn-ghost btn-circle mr-3">
    <div class="indicator">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        ><path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
        /></svg
      >
      <span class="badge badge-xs badge-primary indicator-item"></span>
    </div>
  </button>
  <div class="flex-none gap-2">
    <div class="dropdown dropdown-end">
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
        <div class="w-10 rounded-full">
          <img
            alt="Tailwind CSS Navbar component"
            src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
          />
        </div>
      </div>
      <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
        <li>
          <a href="/profile" class="justify-between text-xl" on:click={myProfile}>
            Profile
            <span class="badge">New</span>
          </a>
        </li>
        <li><a href="/settings" class="text-xl">Settings</a></li>
        <li><a class="text-xl" on:click={logout}>Logout</a></li>
      </ul>
    </div>
  </div>
</div>
