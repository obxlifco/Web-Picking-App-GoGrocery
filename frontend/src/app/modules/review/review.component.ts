import { Component, OnInit, Input } from '@angular/core';


@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {
  showclass:boolean;
  @Input('productId') public product_id ;
  constructor() { }

  ngOnInit() {
  }
  showform(event) {
    this.showclass = event;
  }
  onResetClick(event){
    this.showclass = event;
  }
}
