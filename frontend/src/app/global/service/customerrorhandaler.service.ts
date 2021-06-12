import {Optional, Injectable, ErrorHandler,Inject} from '@angular/core';

@Injectable()
export class CustomErrorHandlerService extends ErrorHandler{

  constructor( @Optional() @Inject('ERROR_WRAPPER') private errorWrapper: any ) { 
  	super();

  }

  handleError(error: Error) {

    console.log('Custom Error Handler error: ' + error.toString());
    if(this.errorWrapper)//serverSide
    {
        this.errorWrapper.error = error;
    }
  }

}