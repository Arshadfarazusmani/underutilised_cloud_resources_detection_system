// Async-handler will create a methord and will export it to use in other files.

const  asyncHandler = (requestHandler) =>{
   return (req,res,next)=>{
        Promise.resolve(requestHandler(req,res,next)).catch((err) => next(err))
    }
}

export {asyncHandler}


// provides the error management by automatically catching promiss regection and passing next 