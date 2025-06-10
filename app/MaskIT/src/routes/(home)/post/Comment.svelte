<script>
    import moment from 'moment';
    import { jwtDecode } from "jwt-decode";

    export let data, parentID, postID;
    let isbox = false;
    console.log(data);

    let loading_comment = false;
    let body = "";

    function convertTime(timestamp) {
    return moment(timestamp).fromNow();
  }

  async function comment() {
    if (body==""){return}
    loading_comment = true
    const response = await fetch('http://127.0.0.1:5000/CreateComment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization':  localStorage.getItem("token")
      },
      body: `reply_id=${data["COMMENT_ID"]}&post_id=${postID}&text=${body}&user_id=${jwtDecode(localStorage.getItem("token"))["sub"]}`,
    });
  
    
    if (!response.error) {
      const responseData = await response.json();
      loading_comment = false;
      data["REPLIES"].unshift(responseData);
      data["REPLIES"] = data["REPLIES"];
      isbox = false;
      body = "";
      if (responseData.error){
        console.log(responseData.error);
      }

    } else {
      // Request failed, handle the error
      console.error('Request failed');
    }
  }

  let curReaction = 0;
  
  async function react(comment_id, reaction) {
    if (reaction == curReaction){
        reaction = 0;
        curReaction = 0;
    }
    curReaction = reaction;
    const response = await fetch('http://127.0.0.1:5000/ReactComment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': localStorage.getItem('token')
      },
      body: `comment_id=${comment_id}&reaction_type=${reaction}&user_id=${jwtDecode(localStorage.getItem("token"))["sub"]}`,
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
<div class="border-l-2 border-primary">

            <div class="m-3 " on:click={() => window.location.replace(`/profile/${data["USER_ID"]}`)}>
                <img class="mr-3 w-9 mask mask-circle float-left" src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
                <div class="mt-1">
                    <span class="mr-3 text-xl text-slate-100">{data["USER_ID"]}</span>
                    <span class="mr-3 text-slate-600">{convertTime(data["CREATED_TIME"])}</span>
                </div>
            </div>
            <div>
                <p class="m-1 mt-3 ml-3 w-full text-lg break-words">{data["COMMENT_TEXT"]}</p>
                    <ul class="menu menu-horizontal h-4 m-0">
                        <li>
                            <div class="btn btn-ghost w-8 m-1 {curReaction == 1 ? 'text-accent' : ''}" on:click={() => react(data["COMMENT_ID"], 1)}>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentcolor" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 14h4v7a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-7h4a1.001 1.001 0 0 0 .781-1.625l-8-10c-.381-.475-1.181-.475-1.562 0l-8 10A1.001 1.001 0 0 0 4 14z" /></svg>
                            </div>
                        </li>
                        
                        <li>
                            <div class="w-8 m-0 btn btn-ghost text-xl">{data["SCORE"] + curReaction}</div>
                        </li>
                        <li>
                        <div class="btn btn-ghost w-8 m-1 {curReaction == -1 ? 'text-secondary' : ''}" on:click={() => react(data["COMMENT_ID"], -1)}>
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentcolor" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20.901 10.566A1.001 1.001 0 0 0 20 10h-4V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v7H4a1.001 1.001 0 0 0-.781 1.625l8 10a1 1 0 0 0 1.562 0l8-10c.24-.301.286-.712.12-1.059z" /></svg>
                        </div>
                        </li>
                        {#if !isbox}
                            <li>
                                <div class="w-16 m-1 ml-3 btn btn-ghost p-2" on:click={() => isbox=true}>Reply</div>
                            </li>
                        {/if}
                </ul>
            </div>

            
            {#if isbox}
            <div class="m-5">
                <textarea bind:value={body} class="textarea textarea-primary textarea-lg p-2 pt-1 mb-0 w-full" placeholder="Comment"></textarea>
                <br>
                <div class="mt-2 flex justify-end">
                    <button class="btn btn-ghost btn-sm mr-2" on:click={() => isbox=false}>Cancel</button>
                    <button class="btn btn-primary btn-sm" on:click={comment}>{#if !loading_comment}Reply{:else}<span class="loading loading-infinity loading-md"></span>{/if}</button>
                </div>
            </div>            
            {/if}

            
            {#each data["REPLIES"] as subdata}
            <div class="ml-5">
              <svelte:self parentID={data["COMMENT_ID"]} data={subdata} postID={postID}/>
            </div>
            {/each}
</div>