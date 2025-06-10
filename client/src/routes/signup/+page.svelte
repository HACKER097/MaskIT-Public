<script>
  let email = '';
  let password = '';

  let text = "";

  let loading = false;


  async function handleSubmit(){
    loading = true;
    if (password.length<5){
      text = "Password length must be atleast 5"
      resp.showModal();
      loading = false;
      return
    }
    const response = await fetch('http://127.0.0.1:5000/SignUp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `&password=${password}&email=${email}`,
     });
    
    if (response.ok) {
      loading = false;
      const responseData = await response.json();
      console.log(responseData);
      if (responseData.UsernameError){
	      text = responseData.UsernameError;
	      resp.showModal();
	    return;
      }
      if (responseData.EmailError){
	      text = responseData.EmailError;
	      resp.showModal();
	    return;
      }
      if (responseData.message){
	      text = responseData.message;
	      resp.showModal();
	    return;
      }
      if (responseData.error){
	        text = responseData.error;
	        resp.showModal();
	        return;
      }
    } else {
      // Request failed, handle the error
      console.error('Request failed');
      return
    }

  }

</script>

<div class="hero min-h-screen bg-base-200">
  <div class="hero-content flex-col lg:flex-row-reverse">
    <div class="text-center lg:text-left">
      <h1 class="text-5xl font-bold">M<span class="text-primary">ask</span>IT</h1>
      <p class="py-6">Discover the Unseen, Say the Unspoken. Anonymously Yours, MaskIT​</p>
    </div>
    <div>
      <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
        <form on:submit|preventDefault={handleSubmit} class="card-body"> <!-- preventDefault added here -->
          <div class="form-control">
            <label class="label">
              <span class="label-text">Student email</span>
            </label>
            <input bind:value={email} type="email" placeholder="XXX@learner.manipal.edu" class="input input-bordered" required />
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text">Password</span>
            </label>
            <input bind:value={password} type="password" placeholder="password" class="input input-bordered" required />
            <label class="label">
              <a href="#" class="label-text-alt link link-hover">Forgot password?</a>
            </label>
          </div>
          <div class="form-control mt-6">
            <button type="submit" class="btn btn-primary" on:click={handleSubmit}>{#if !loading}Create{:else}<span class="loading loading-infinity loading-lg"></span>{/if}</button> <!-- type="submit" added here -->
          </div>
        </form>
      </div>
      <div class="card bg-base-100 shadow-xl m-3">
        <div class="card-body">
          <p>Already have an account? <a class="link link-info" href="/login"> Login</a></p>
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