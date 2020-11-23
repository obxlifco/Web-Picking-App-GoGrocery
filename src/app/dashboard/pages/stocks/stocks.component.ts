import { Component, OnInit } from '@angular/core';
import { GlobalitemService } from 'src/app/services/globalitem/globalitem.service';
import { ModalService } from 'src/app/services/modal/modal.service';

@Component({
  selector: 'app-stocks',
  templateUrl: './stocks.component.html',
  styleUrls: ['./stocks.component.scss']
})
export class StocksComponent implements OnInit {

  constructor(private modalservice : ModalService) { }

  ngOnInit(): void {
  }

  opencategory_modal():void{
    this.modalservice.openSubCategoryModal("jamal").then(data =>{
      this.modalservice.closeCategoryModal().then(data =>{
        console.log("category closed Modal : ",data);
      })
    })  
  }

  
  opensub_category_modal():void{
    this.modalservice.openSubCategoryModal("jamal").then(data =>{
      this.modalservice.closeCategoryModal().then(data =>{
        console.log("sub category closed Modal : ",data); 
      })
    })  
  }



}
