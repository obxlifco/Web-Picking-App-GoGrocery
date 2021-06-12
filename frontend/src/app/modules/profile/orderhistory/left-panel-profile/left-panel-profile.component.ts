import { Component, OnInit,Input} from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import { AuthenticationService } from '../../../../global/service/authentication.service';
import { GlobalService } from '../../../../global/service/app.global.service';

@Component({
  selector: 'app-left-panel-profile',
  templateUrl: './left-panel-profile.component.html',
  styleUrls: ['./left-panel-profile.component.css']
})
export class LeftPanelProfileComponent implements OnInit {

  @Input() activatedMenu : string;
  constructor(public authenticationService:AuthenticationService,public _router:Router) { }

  ngOnInit() {


  }
  
  /**
   * Method to navigate to url
   * @access public
   * @param url
  */
  navigateToUrl(url:string) {
  	this._router.navigate([url]);
  }

}
