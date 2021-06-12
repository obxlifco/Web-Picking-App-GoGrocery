import { Component } from '@angular/core';
@Component({
  selector: '<footer-view></footer-view>',
  templateUrl: './templates/footer.html'
})
export class FooterComponent {
  public currentDate:any = new Date();
}