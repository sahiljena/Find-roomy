function send() {
    var x = document.getElementById("otpsend");
    var check = document.getElementById("check");
    if (x.innerHTML === "Send OTP" || x.innerHTML === "Re - Send") {
      x.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Sending...';
      x.disabled = true;
      var url = "sendotp?tname="
      var tname = document.getElementById("exampleFormControlInput1").value;
      console.log(tname);
      var url = url+tname;
      fetch(url).then(res => res.json()).then(data => {
        if(data.data === "Please use mail id with the domain 'srmist.edu.in' only" || data.data === "Unexpected error occured while delivering OTP please try again later"){
            check.innerHTML = `<br><h6 style='color: red;'> *${data.data}</h6>`
            x.innerHTML = 'Send OTP';
            x.disabled = false;
        }else{
        check.innerHTML = '<form method="POST" action="#"><div class="form-group"><label for="otp">OTP</label><input type="number" class="form-control" id="otp" placeholder="****" name="OTP" required></div><button type="submit" class="btn btn-dark btn-sm align-middle btn-lg btn-block" id="checkotp" >Verify</button></form>';
        x.innerHTML = 'Re - Send';
        x.disabled = false;
        }
      });
      
    }
  }

document.onreadystatechange = function() { 
    if (document.readyState !== "complete") { 
        document.querySelector("body").style.visibility = "hidden"; 
        document.querySelector("#loader").style.visibility = "visible"; 
    } else { 
        document.querySelector("#loader").style.display = "none"; 
        document.querySelector("body").style.visibility = "visible"; 
    } 
};
bootbox.alert("<h5 style='padding: 10px;'>To reduce spams you can add your hostel data <b>only once!</b><br> So be carefull you <b style='color: #ff005d;'>dumbass!</h5><br><img class='lazy' width='100' src='https://avatars3.githubusercontent.com/u/36576810?s=280&v=4'>"); 