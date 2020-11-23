import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Router, NavigationEnd } from '@angular/router';
import { ApiService } from './services/api/api.service';
import { DatabaseService } from './services/database/database.service';
import { GlobalitemService } from './services/globalitem/globalitem.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'lifco Picking pp';
  loginRouterLink: any
  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  constructor(private breakpointObserver: BreakpointObserver,
    private router: Router,
    private apiService: ApiService,
    public globalitems:GlobalitemService,
    private db:DatabaseService
  ) {
    console.log("router link : ", this.loginRouterLink);
    router.events.subscribe((url: any) =>
      this.getURL(url.url)
    );

    this.initializeMethod()
  }

  initializeMethod(){
    this.isuerlogin()
  }
  getURL(url?: any) {
    this.loginRouterLink = url?.url
    console.log("router link : ", this.loginRouterLink);
  }

  isuerlogin(){
    this.apiService.getIPAddress().subscribe(data =>{  
      console.log("Ip Address : ",data);   
      this.db.setIP(data)
    })
  }
  logout(){
    this.globalitems.showSuccess("You have Sucessfully logout","Success")
    this.db.SignOut();
    this.router.navigate(["login"])
  }
}
