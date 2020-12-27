import { Component, Inject, OnInit } from '@angular/core';
// import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import doc from 'jspdf-autotable';
import { DOCUMENT } from '@angular/common';

declare var $:any
declare var jsPDF: any;
@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent implements OnInit {

  constructor(@Inject(DOCUMENT) private document: Document) {
    // this.goToUrl()
   }

  ngOnInit(): void {
  }
  generatePdf(){
    var doc :any = new jsPDF();
var elementHTML = $('#imgTable').html();
var specialElementHandlers = {
    '#elementH': function (element:any, renderer:any) {
        return true;
    }
};
doc.fromHTML(elementHTML, 15, 15, {
    'width': 170,
    'elementHandlers': specialElementHandlers
});

// Save the PDF
  doc.save('sample-document.pdf');
    }
    
    goToUrl(): void {
      this.document.location.href = 'https://stackoverflow.com';
  }
}