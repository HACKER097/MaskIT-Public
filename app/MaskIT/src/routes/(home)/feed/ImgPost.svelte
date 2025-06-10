<script>
  import { jwtDecode } from "jwt-decode";
  import moment from 'moment';
  export let PostData;


  function convertTime(timestamp) {
    return moment(timestamp).fromNow();
  }

  
  let curReaction = 0;
  
  async function react(post_id, reaction) {
    if (reaction == curReaction){
      reaction = 0;
      curReaction = 0;
    }
    curReaction = reaction;
    const response = await fetch('http://127.0.0.1:5000/ReactPost', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': localStorage.getItem('token')
      },
      body: `post_id=${post_id}&reaction_type=${reaction}&user_id=${jwtDecode(localStorage.getItem("token"))["sub"]}`,
    });
  
    
    if (response.ok) {
      const responseData = await response.json();
      if (!responseData.message){
        curReaction = 0;
      } 
    } else {
      // Request failed, handle the error
      console.error('Request failed');
    }
  }
</script>

<div class="card bg-base-100 mb-0 mt-5 border-0">
  <div class="m-3" on:click={() => window.location.replace(`/profile/${PostData[1]}`)}>
    <img class="mr-3 w-9 mask mask-circle float-left" src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
    <div class="mt-1">
        <span class="mr-3 text-slate-100">{PostData[1]}</span>
        <span class="mr-3 text-slate-600">{convertTime(PostData[6])}</span>
    </div>
</div>
<div class="flex flex-row">
  {#if PostData[3]!=""}
  {#each PostData[3].split(",") as tag}
  <span class="badge badge-accent badge-outline m-3 mr-1 mt-1">{tag}</span>
  {/each}
  {/if}
</div>
<a href="/post/{PostData[0]}">
<figure>
  <img
  class="w-full"
  src={PostData[5]}
  />
</figure>
{#if PostData[4]!=""}
  <div class="badge badge-secondary badge-outline 0 m-2 mb-0 mt-1">{PostData[4]}</div>
{/if}
<p class="p-2">{PostData[2]}</p>
</a>
<div class="card-body p-1">
  <div class="card-actions">
    <button class="btn btn-ghost btn-square m-0 w-8 {curReaction == 1 ? 'text-accent' : ''}" on:click={() => react(PostData[0], 1)}>
      <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="currentcolor"
          viewBox="0 0 24 24"
          stroke="currentColor"
          ><path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1"
            d="M4 14h4v7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7h4a1.001 1.001 0 0 0 .781-1.625l-8-10c-.381-.475-1.181-.475-1.562 0l-8 10A1.001 1.001 0 0 0 4 14z"
          /></svg
        >
      </button>
      <div class="btn btn-ghost btn-square text-xl w-8">{PostData[7] + curReaction}</div>
      <button class="btn btn-ghost btn-square w-8 {curReaction == -1 ? 'text-secondary' : ''}" on:click={() => react(PostData[0], -1)}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="currentcolor"
          viewBox="0 0 24 24"
          stroke="currentColor"
          ><path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1"
            d="M20.901 10.566A1.001 1.001 0 0 0 20 10h-4V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v7H4a1.001 1.001 0 0 0-.781 1.625l8 10a1 1 0 0 0 1.562 0l8-10c.24-.301.286-.712.12-1.059z"
          /></svg
        >
      </button>
    </div>
  </div>
</div>
