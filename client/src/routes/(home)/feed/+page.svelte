<script>
  import { onMount } from "svelte";
  import ImgPost from "./ImgPost.svelte";
  import TextPost from "./TextPost.svelte";

  let feedData;
  let feedData_time;
  let loading = true;

  

  onMount(async () => {
    let cachelife = 10*5;

    feedData = JSON.parse(localStorage.getItem("feedData"));
    feedData_time = localStorage.getItem("feedData_time");
    
    if (feedData && (parseInt(Date.now() / 1000) - parseInt(feedData_time) < cachelife)) {
      feedData = feedData;
      loading = false;
    }else{
      console.log(feedData)
      try {
        const response = await fetch('http://127.0.0.1:5000/GetFeed', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({}) 
        });
  
        if (response.ok) {
          feedData = await response.json();
          loading = false;
          localStorage.setItem("feedData", JSON.stringify(feedData));
          localStorage.setItem("feedData_time", parseInt(Date.now() / 1000))
        } 
      } catch (error) {
        console.error('Failed to fetch feed:', error);
      }
    }

  });


  
</script>

<div class="content-center" >
  {#if loading}
    {#each [1, 2, 3] as _, i}
      <div class="flex flex-col gap-4 w-full mb-4">
        <div class="flex gap-4 items-center">
          <div class="skeleton w-16 h-16 rounded-full shrink-0"></div>
          <div class="flex flex-col gap-4">
            <div class="skeleton h-4 w-20"></div>
            <div class="skeleton h-4 w-28"></div>
          </div>
        </div>
        <div class="skeleton h-96 w-full"></div>
      </div>
    {/each}
  {:else}
    {#each feedData as PostData, i}
      {#if PostData[5] != null}
        <ImgPost {PostData} />
      {:else}
        <TextPost {PostData} /> 
      {/if}
      <div class="divider m-0"></div>
    {/each}
  {/if}
</div>
