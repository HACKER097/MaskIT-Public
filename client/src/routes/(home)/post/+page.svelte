<script>
    /** @type {import('./$types').PageData} */
    export let data;
    import ImgPost from '../feed/ImgPost.svelte';
    import Comment from './Comment.svelte';
</script>



  <ImgPost />

  <div class="divider m-0"></div> 

<Comment level={1} text={"Hello everyone, you was your day?"}/>
<Comment level={5} text={"YOUR MOM's A HOE"}/>
