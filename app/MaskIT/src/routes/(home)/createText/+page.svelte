<script>
    /** @type {import('./$types').PageData} */
    export let data;

    import { jwtDecode } from "jwt-decode";

    let loc = "";
    let tags = ["Funny", "Sad", "Rant", "Meme", "Casual"];
    let seltags = [];
    let title = "";
    let body = "";

    let loading = false;


    async function post() {

  loading = true;

  const formData = new FormData();
      formData.append('user_id', jwtDecode(localStorage.getItem("token"))["sub"]);
      formData.append('caption', title);
      formData.append('tags', seltags.join(","));
      formData.append('location', loc);
      formData.append('body', body);

  try {
    const response = await fetch('http://127.0.0.1:5000/CreatePost', {
      method: 'POST',
      headers: {
        'Authorization': localStorage.getItem("token")
      },
      body: formData
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const responseData = await response.json();
    if (responseData.message){
      loading = false;
      window.location.replace("/feed")
    }


  } catch (error) {
    console.error('Request failed:', error);
  }
}

</script>

<div class="mt-4 flex items-center justify-center flex-col ">
    <div class="card w-11/12 bg-base-100 shadow-xl h-11/12">

      <div class="card-body overflow-scroll">
          <input bind:value={title} type="text" placeholder="Title" class="input input-bordered input-primary w-full mt-4" />
            {#if loc!=""}
                <div class="badge badge-secondary badge-outline">{loc}</div>
            {/if}
            {#if seltags!=[]}
            <div class="flex flex-row">
                {#each seltags as seltag}
                    <span class="badge badge-accent badge-outline  mr-1">{seltag}</span>
                {/each}
            </div>
            {/if}
          <div class="card-actions justify-end">
            <textarea bind:value={body} class="textarea textarea-md textarea-primary w-full mt-4 h-64" placeholder="Text"></textarea>
            <button class="btn btn-outline btn-primary w-full mt-4 " onclick="location_popup.showModal()">Location</button>
            <button class="btn btn-primary w-full mt-4 btn-outline" onclick="tags_popup.showModal()">Tags</button>
            <button class="btn btn-primary mt-4 w-full mb-16" on:click={() => post()}>{#if !loading}POST{:else}<span class="loading loading-infinity loading-lg"></span>{/if}</button>
        </div>
    </div>
</div>


</div>

<dialog id="location_popup" class="modal modal-bottom">
    <div class="modal-box h-9/12">
        {#each {length: 15} as _, i}
        <button class="btn btn-primary w-full mt-4 btn-outline" onclick="location_popup.close()" on:click={() => loc=`Location ${i+1}`}>Location {i+1}</button>
        {/each}
    </div>

	<form method="dialog" class="modal-backdrop">
		<button>close</button>
	  </form>
</dialog>

<dialog id="tags_popup" class="modal modal-bottom">
    <div class="modal-box h-9/12">
        {#each tags as tag}
        {#if seltags.includes(tag)}
          <button class="btn btn-primary w-full mt-4" on:click={() => seltags = seltags.filter(item => item !== tag)}>{tag}</button>
        {:else}
          <button class="btn btn-primary w-full mt-4 btn-outline" on:click={() => seltags = [...seltags, tag]}>{tag}</button>
        {/if}
      {/each}
    </div>

	<form method="dialog" class="modal-backdrop">
		<button>close</button>
	  </form>
</dialog>

