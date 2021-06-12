import { Component, OnInit } from '@angular/core';
import {LoaderService} from '../../service/loader.service';
import {GlobalService} from '../../service/app.global.service';
import {Subject,Observable} from 'rxjs';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.css']
})
export class LoaderComponent implements OnInit {
  color = 'primary';
  mode = 'indeterminate';
  value = 500;
  public isLoading$:Observable<boolean>;
  
  constructor(private _loader:LoaderService,private _globalService:GlobalService) {
    

   }

  ngOnInit() {
    this.isLoading$ =  this._globalService.loadSpinnerChange$;

  }

}
