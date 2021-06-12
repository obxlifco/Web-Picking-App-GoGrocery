import { Injectable } from "@angular/core";
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest,HttpResponse} from "@angular/common/http";
/*import {HttpRequest} from '@angular/http';*/
import { Observable } from "rxjs";
import { finalize } from "rxjs/operators";
import { tap } from "rxjs/operators";

import { LoaderService } from '../../global/service/loader.service';

@Injectable()
export class LoaderInterceptor implements HttpInterceptor {
    constructor(public loaderService: LoaderService) { }
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        //this.loaderService.show();
        return next.handle(req).pipe(tap(evt => {
		      if (evt instanceof HttpResponse) {
		        //this.loaderService.hide();
		      }
      }));
        /*return next.handle(req).pipe(
            finalize(() => this.loaderService.hide())
        );*/
    }
}