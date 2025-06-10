<script>
    /** @type {import('./$types').PageData} */
    export let data;
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import ImgPost from '../../feed/ImgPost.svelte';
    import TextPost from "../../feed/TextPost.svelte";
    import Comment from '../Comment.svelte';
    import { jwtDecode } from "jwt-decode";
    
    const postID = $page.params.postID;
    let loading = true;
    let loading_tree = true;

    let loading_comment = false;
    let body = "";

    let PostData;
    let CommentTree;


onMount(async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/GetPost', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `post_id=${postID}`
    });

    if (response.ok) {
      PostData = await response.json();
      console.log(PostData);
      loading = false;
    } 
  } catch (error) {
    console.error('Failed to fetch post:', error);
  }
  console.log(PostData);
  try {
    const response = await fetch('http://127.0.0.1:5000/GetCommentTree', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `post_id=${postID}`
    });

    if (response.ok) {
      CommentTree = await response.json();
      console.log(CommentTree);
      loading_tree = false;
    } 
  } catch (error) {
    console.error('Failed to fetch tree:', error);
  }
});

async function comment() {
    if (body==""){return}
    loading_comment = true
    const response = await fetch('http://127.0.0.1:5000/CreateComment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization':  localStorage.getItem("token")
      },
      body: `post_id=${postID}&text=${body}&user_id=${jwtDecode(localStorage.getItem("token"))["sub"]}`,
    });
  
    
    if (!response.error) {
      const responseData = await response.json();
      loading_comment = false;
      CommentTree.unshift(responseData);
      body = "";
      CommentTree = CommentTree;
      if (responseData.error){
        console.log(responseData.error);
      }

    } else {
      // Request failed, handle the error
      console.error('Request failed');
    }
  }
  

</script>

{#if loading}
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
  {:else}
    {#if PostData[5] != null}
        <ImgPost {PostData} />
    {:else}
        <TextPost {PostData} /> 
    {/if}

{/if}

<div class="divider m-0"></div> 

<div class="m-5 mb-10">
    <textarea bind:value={body} class="textarea textarea-primary textarea-lg p-2 pt-1 mb-0 w-full" placeholder="Reply"></textarea>
    <br>
    <div class="mt-2 flex justify-end">
        <button class="btn btn-ghost btn-sm mr-2">Cancel</button>
        <button class="btn btn-primary btn-sm" on:click={comment}>{#if !loading_comment}Reply{:else}<span class="loading loading-infinity loading-md"></span>{/if}</button>
    </div>
</div>            



{#if loading_tree}
<div class="flex flex-col gap-4 w-full m-4">
  <div class="flex gap-4 items-center">
    <div class="skeleton w-16 h-16 rounded-full shrink-0"></div>
    <div class="flex flex-col gap-4">
      <div class="skeleton h-4 w-60"></div>
      <div class="skeleton h-4 w-56"></div>
    </div>
  </div>
</div>
<div class="flex flex-col gap-4 w-full m-4">
  <div class="flex gap-4 items-center">
    <div class="skeleton w-16 h-16 rounded-full shrink-0"></div>
    <div class="flex flex-col gap-4">
      <div class="skeleton h-4 w-52"></div>
      <div class="skeleton h-4 w-56"></div>
    </div>
  </div>
</div>

{:else}
{#each CommentTree as data}
<div class="w-full overflow-hidden">
  <Comment parentID={null} data={data} postID={postID}/>
</div>
{/each}
{/if}