class api_error extends Error {
  constructor(
     statuscode,
    message="An error occurred while processing your request",
     error=[],
    stack="" ) {
    super(message);
    this.statuscode = statuscode;
   this.message = message;
   this.data= null;
   this.success = false;
   this.error= error;

   if (stack) {
     this.stack = stack;
   } else { 
     Error.captureStackTrace(this, this.constructor);
   }
  }
}

export { api_error };