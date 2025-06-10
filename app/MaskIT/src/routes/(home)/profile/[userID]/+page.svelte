<script>
  /** @type {import('./$types').PageData} */
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { jwtDecode } from "jwt-decode";
  const userID = $page.params.userID;
  let data = [];

  let loading = true;

  onMount(async () => {
  let cachelife = 10;
  data = JSON.parse(localStorage.getItem(`Profile/${userID}`));
  let data_time = localStorage.getItem(`Profile/time/${userID}`);
  console.log(data_time);
  console.log(parseInt(Date.now()) / 1000);

  if ((parseInt(Date.now()) / 1000 - data_time < cachelife)){
    console.log("OK");
    loading = false;
  }else{
    try {
      const response = await fetch('http://127.0.0.1:5000/GetProfile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${userID}`
      });

      if (response.ok) {
        data = await response.json();
        console.log(data);
        localStorage.setItem(`Profile/${userID}`, JSON.stringify(data));
        localStorage.setItem(`Profile/time/${userID}`, parseInt(Date.now() / 1000));
        loading = false;
      } 
    } catch (error) {
      console.error('Failed to fetch feed:', error);
    }
  }

  console.log(data[0]);
  data = data;

});

</script>
{#if loading}
<div class="flex flex-col gap-4 w-full">
  <div class="flex justify-center items-center">
    <div class="skeleton w-52 h-52 rounded-full shrink-0"></div>
  </div>
  <div class="skeleton h-96 w-full"></div>
</div>
{:else}
<div class="border-2 m-2 rounded-xl">
    <div class="divider mt-32 mb-28 ">
        <div class="w-96 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
            <div class="mask mask-circle ">
                <img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
            </div>
        </div>
    </div>
    <h1 class="text-3xl text-center">{userID}</h1>
    <div class="stats shadow w-full stats-vertical sm:stats-horizontal">
        
        <div class="stat place-items-center">
            <div class="stat-title">Posts</div>
            <div class="stat-value">{data[0]}</div>
            <div class="stat-desc">Since January 1st</div>
        </div>
        
        <div class="stat place-items-center">
            <div class="stat-title">Karma</div>
            <div class="stat-value text-secondary">{data[2]}</div>
            <div class="stat-desc text-secondary">↗︎ 40 (2%)</div>
        </div>
        
        <div class="stat place-items-center">
            <div class="stat-title">Comments</div>
            <div class="stat-value">{data[1]}</div>
            <div class="stat-desc">↘︎ 90 (14%)</div>
        </div>
        
    </div>
</div>
{/if}