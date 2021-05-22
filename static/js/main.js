const form = document.getElementById('form');
const name1 = document.getElementById('name');
const email = document.getElementById('email');
const rollNo = document.getElementById('roll-no');
const password = document.getElementById('password1');
const confirmPassword = document.getElementById('password2');

//SHOW'S INPUT ERROR MESSAGE
function showError(input, message)
{
    const inputGroup = input.parentElement;
  input.className = 'form-control error';
  alert(message);
}

//shows input success
function showSuccess(input)
{
  input.className = 'form-control success';
}

//check Email isValid
function emailIsValid(email){
    //const regx = /^([a-zA-Z0-9\.]+)@([v i t]{3}+).([e d u]{3}+).([i n]{2})$/;
    const regx = /^([A-Za-z0-9_\-\.])+\@([v i t 0-3_\-\.])+\.([e d u]{3})+\.([i n]{2})$/;
    return regx.test((email).toLowerCase());
}
//rollno is valid
function rollNoIsValid(rollNo) {
    const regx2 = /^([1-9][0-9]{4}[A-Z][0-9]{4})$/;
    return regx2.test(rollNo);
}

//event listeners
form.addEventListener('submit',function(e){
    e.preventDefault();

    if(name1.value === '')
   {
        showError(name1, 'Name is Required')
    }
    else{
        showSuccess(name1)
    }

    if(email.value === '')
    {
         showError(email, 'Email is Required')
     } 
     else if(!emailIsValid(email.value))
     {
        showError(email, 'Email is not VIT mail')
     }
     else{
         showSuccess(email)
     }

     if(rollNo.value === '')
     {
          showError(rollNo, 'Roll-no is Required')
      }
      else if(!rollNoIsValid(rollNo.value))
     {
        showError(rollNo, 'rollNo doesnt belong to vit')
     }
      
      else{
          showSuccess(rollNo)
      }

      if(password.value === '')
      {
           showError(password, 'Password is Required')
       }
       else{
           showSuccess(password)
       }

       if(confirmPassword.value === '')
       {
           
            showError(confirmPassword, 'Password is required')
        }
        else{
            showSuccess(confirmPassword)
        }


})