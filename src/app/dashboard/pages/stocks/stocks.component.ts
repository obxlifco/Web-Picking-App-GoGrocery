import { Component, OnInit } from '@angular/core';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';

@Component({
  selector: 'app-stocks',
  templateUrl: './stocks.component.html',
  styleUrls: ['./stocks.component.scss']
})
export class StocksComponent implements OnInit {

  constructor(private globalitem : GlobalitemService) { }

  ngOnInit(): void {
  }

  opencategory_modal():void{
    this.globalitem.openSubCategoryModal("jamal").then(data =>{
      this.globalitem.closeCategoryModal().then(data =>{
        console.log("category closed Modal : ",data);
      })
    })  
  }

  
  opensub_category_modal():void{
    this.globalitem.openSubCategoryModal("jamal").then(data =>{
      this.globalitem.closeCategoryModal().then(data =>{
        console.log("sub category closed Modal : ",data); 
      })
    })  
  }



}
