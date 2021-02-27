import { Injectable, isDevMode } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { DatabaseService } from 'src/app/services/database/database.service';
import { CSVRecord } from './csvrecord';

export interface PaymentMethodInter {
  name: string;
  completed: boolean;
  id: any;
  type: any
  color: ThemePalette;
  subtasks?: PaymentMethodInter[];
}

@Injectable({
  providedIn: 'root'
})
export class CommonfunctionService {
  counter = 0;
  pdfMake: any;
  public records: any[] = [];

  constructor(public db: DatabaseService) { }
  public warehouse_id: any = ''
  public website_id: any = ''
  data = {
    warehouse_id: '',
    website_id: ''
  }

  headerlist: any
  set setWarehouseIDS(val: any) {
    this.db.getUserData().then(res => {
      // console.log("user data inside dashboard : ", res);
      this.data.warehouse_id = res.warehouse_id,
        this.data.website_id = res.website_id
    })
  }
  get getWarehouseIDS(): any {
    return this.data;
  }

  getcompletedOrders(completeorderdata: any, paymentid: any): any {
    let shpcost: any = 0;
    let subtotal: any = 0;
    let grandtotal: any = 0;
    let shippingdiscount: any = 0;
    let coupendiscount: any = 0;
    let counters: any = 0
    for (var i = 0; i < completeorderdata.length; i++) {
      if (!completeorderdata[i]?.customer?.first_name?.includes("Test") && !completeorderdata[i]?.customer?.first_name?.includes("test") &&
        !completeorderdata[i]?.customer?.last_name?.includes("Test") && !completeorderdata[i]?.customer?.last_name?.includes("test")) {
        // console.log("name entered is : ",completeorderdata[i].customer.first_name);

        shpcost += completeorderdata[i].shipping_cost
        subtotal += completeorderdata[i].net_amount
        grandtotal += completeorderdata[i].gross_amount
        shippingdiscount += completeorderdata[i].cart_discount
        coupendiscount += completeorderdata[i].gross_discount_amount
      } else {
        counters++
        // console.log("test name entered is : ",completeorderdata[i].customer.first_name);
      }
      // console.log("shpcost : ",shpcost," subtotal:",subtotal," grandtotal: ",grandtotal);
    }
    let data = {
      shpcost: shpcost,
      subtotal: subtotal,
      grandtotal: grandtotal,
      totalList: completeorderdata,
      testorderFound: counters,
      shippingdiscount: shippingdiscount,
      coupendiscount: coupendiscount
    }
    return data
  }

  //round off price
  precise_round(num: any, decimals: any) {
    var t = Math.pow(10, decimals);
    return (Math.round((num * t) + (decimals > 0 ? 1 : 0) * (Math.sign(num) * (10 / Math.pow(100, decimals)))) / t).toFixed(decimals);
  }

  //download csv file

  //convert json to csv and download it
  downloadFile(data: any, filename = 'picker list', dataparams: any, footerdata: any) {
    // console.log("data : ", data, "params : ", dataparams);
    let csvData = this.ConvertToCSV(data, dataparams);
    // console.log("csvData", csvData + '\r\n'+" Total Amount,"+"ordernum,"+"orderdate,"+"cname,"+"pmethod,"+"122323,"+"123,"+"0,"+"11,"+"333432211" ," header list :",this.headerlist)
    if (filename === "order products") {
      csvData = csvData + '\r\n' + " Total Amount," + "," + "," + "," + "," + footerdata.Subtotal + "," + footerdata.ShippingCost + "," + footerdata.ShippingDiscount + "," + footerdata.OtherDiscount + "," + footerdata.GrandTotal
    }
    let blob = new Blob(['\ufeff' + csvData], { type: 'text/csv;charset=utf-8;' });
    let dwldLink = document.createElement("a");
    let url = URL.createObjectURL(blob);
    let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
    if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
    }
    dwldLink.setAttribute("href", url);
    dwldLink.setAttribute("download", filename + ".csv");
    dwldLink.style.visibility = "hidden";
    document.body.appendChild(dwldLink);
    dwldLink.click();
    document.body.removeChild(dwldLink);
  }
  ConvertToCSV(objArray: any, headerList: any) {
    let array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    let str = '';
    let row = 'S.No,';
    for (let index in headerList) {
      row += headerList[index] + ',';
    }
    row = row.slice(0, -1);
    this.headerlist = row
    str += row + '\r\n';
    for (let i = 0; i < array.length; i++) {
      let line = (i + 1) + '';
      for (let index in headerList) {
        let head = headerList[index];
        line += ',' + array[i][head];
      }
      str += line + '\r\n';
    }
    return str;
  }

  monthname: any = [
    {
      "abbreviation": "Jan",
      "name": "January"
    },
    {
      "abbreviation": "Feb",
      "name": "February"
    },
    {
      "abbreviation": "Mar",
      "name": "March"
    },
    {
      "abbreviation": "Apr",
      "name": "April"
    },
    {
      "abbreviation": "May",
      "name": "May"
    },
    {
      "abbreviation": "Jun",
      "name": "June"
    },
    {
      "abbreviation": "Jul",
      "name": "July"
    },
    {
      "abbreviation": "Aug",
      "name": "August"
    },
    {
      "abbreviation": "Sep",
      "name": "September"
    },
    {
      "abbreviation": "Oct",
      "name": "October"
    },
    {
      "abbreviation": "Nov",
      "name": "November"
    },
    {
      "abbreviation": "Dec",
      "name": "December"
    }
  ]

  filterArray(array: any = []): any {
    return array.filter(function (elem: any, index: any, self: string | any[]) {
      return index === self.indexOf(elem);
    })
  }

  //convert html to pdf
  generatePDF(elementID: any, pdfName: any) {
    html2canvas(elementID, { useCORS : false,allowTaint: false,logging: true,imageTimeout: 20000}).then(canvas => {
      let HTML_Width = canvas.width;
      let HTML_Height = canvas.height;
      let top_left_margin = 15;
      let PDF_Width = HTML_Width + (top_left_margin * 2);
      let PDF_Height = (PDF_Width * 1.5) + (top_left_margin * 2);
      let canvas_image_width = HTML_Width;
      let canvas_image_height = HTML_Height;
      let totalPDFPages = Math.ceil(HTML_Height / PDF_Height) - 1;
      canvas.getContext('2d');
      let imgData = canvas.toDataURL("image/png;", 10)
      let pdf = new jsPDF('p', 'pt', [PDF_Width, PDF_Height]);
      pdf.addImage(imgData, 'PNG', top_left_margin, top_left_margin, canvas_image_width, canvas_image_height);
      for (let i = 1; i <= totalPDFPages; i++) {
        pdf.addPage([PDF_Width, PDF_Height], 'p');
        pdf.addImage(imgData, 'PNG', top_left_margin, -(PDF_Height * i) + (top_left_margin * 4), canvas_image_width, canvas_image_height);
      }
      console.log("reached");
      
      pdf.save(pdfName + ".pdf");
    });
  }

  //import bulk products
  async getRecord() {
    return this.records
  }
  // uploadListener($event: any) {
  //   let text = [];
  //   let files = $event.srcElement.files;
  //   if (this.isValidCSVFile(files[0])) {
  //     let input = $event.target;
  //     let reader = new FileReader();
  //     reader.readAsText(input.files[0]);
  //     reader.onload = () => {
  //       let csvData = reader.result;
  //       let csvRecordsArray = (<string>csvData).split(/\r\n|\n/);

  //       let headersRow = this.getHeaderArray(csvRecordsArray);

  //       this.records = this.getDataRecordsArrayFromCSVFile(csvRecordsArray, headersRow.length);
  //       console.log("records : ", this.records);
  //       // return this.records
  //     };
  //     reader.onerror = function () {
  //       console.log('error is occured while reading file!');
  //     };

  //   } else {
  //     alert("Please import valid .csv file.");
  //     this.fileReset();
  //   }
  //   // return this.records

  // }

  // getDataRecordsArrayFromCSVFile(csvRecordsArray: any, headerLength: any) {
  //   let csvArr = [];

  //   for (let i = 1; i < csvRecordsArray.length; i++) {
  //     let curruntRecord = (<string>csvRecordsArray[i]).split(',');
  //     if (curruntRecord.length == headerLength) {
  //       let csvRecord: CSVRecord = new CSVRecord();
  //       console.log("csv file data : ", curruntRecord);
  //       csvRecord.productName = curruntRecord[0];
  //       csvRecord.sku = curruntRecord[1];
  //       csvRecord.parentsku = curruntRecord[2];
  //       csvRecord.size = curruntRecord[3]?.trim();
  //       csvRecord.colour = curruntRecord[4]?.trim();
  //       csvRecord.brand = curruntRecord[5]?.trim();
  //       csvRecord.largdescription = curruntRecord[6];
  //       csvRecord.smalldescription = curruntRecord[7];
  //       csvRecord.features = curruntRecord[8];
  //       csvRecord.saletaxclass = curruntRecord[9]?.trim();
  //       csvRecord.grossweight = curruntRecord[10]?.trim();
  //       csvRecord.price = curruntRecord[11]?.trim();
  //       csvRecord.barcode = curruntRecord[12];
  //       csvRecord.metapagetitle = curruntRecord[13];
  //       csvRecord.maetakeyword = curruntRecord[14];
  //       csvRecord.metadescription = curruntRecord[15]?.trim();
  //       csvRecord.metapageurl = curruntRecord[16]?.trim();
  //       csvRecord.image1 = curruntRecord[17]?.trim();
  //       csvRecord.image2 = curruntRecord[18];
  //       csvRecord.image3 = curruntRecord[19];
  //       csvRecord.image4 = curruntRecord[20];
  //       csvRecord.image5 = curruntRecord[21]?.trim();
  //       csvRecord.hsncode = curruntRecord[22]?.trim();
  //       csvRecord.maxorderunit = curruntRecord[23]?.trim();
  //       csvRecord.unitofmeasurment = curruntRecord[24]?.trim();
  //       csvArr.push(csvRecord);
  //     }
  //   }
  //   return csvArr;
  // }

  // isValidCSVFile(file: any) {
  //   return file.name.endsWith(".csv");
  // }

  // getHeaderArray(csvRecordsArr: any) {
  //   let headers = (<string>csvRecordsArr[0]).split(',');
  //   let headerArray = [];
  //   for (let j = 0; j < headers.length; j++) {
  //     headerArray.push(headers[j]);
  //   }
  //   return headerArray;
  // }

  fileReset() {
    // this.csvReader.nativeElement.value = "";  
    this.records = [];
  }

  generalDownloadfile(url: any) {
    let dwldLink = document.createElement("a");
    let isSafariBrowser = navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1;
    if (isSafariBrowser) {  //if Safari open in new window to save file with random filename.
      dwldLink.setAttribute("target", "_blank");
    }
    dwldLink.setAttribute("href", url);
    // dwldLink.setAttribute("download", filename + ".csv");
    dwldLink.style.visibility = "hidden";
    document.body.appendChild(dwldLink);
    dwldLink.click();
    document.body.removeChild(dwldLink);
  }

  //this function will check the file is in correct formate for bulk product price and stock
  isFileAllowed(fileName: string) {
    let isFileAllowed = false;
    const allowedFiles = ['.xls', '.xlsx',];
    const regex = /(?:\.([^.]+))?$/;
    const extension = regex.exec(fileName);
    if (isDevMode()) {
      console.log('extension du fichier : ', extension);
    }
    if (undefined !== extension && null !== extension) {
      for (const ext of allowedFiles) {
        if (ext === extension[0]) {
          isFileAllowed = true;
        }
      }
    }
    return isFileAllowed;
  }
  // payment method
  getPaymentMethod():any{
   let primarycolor: any = "#007bff"
  let  paymentmethod: PaymentMethodInter = {
      name: 'Online Payment/Cash Payment',
      type: "Select All",
      completed: false,
      color: primarycolor,
      id: 'both',
      subtasks: [
        { name: 'Cash On Delivery', id: 16, type: "Cash On Delivery", completed: true, color: 'primary' },
        { name: 'Card On Delivery', id: 59, type: "Card On Delivery", completed: true, color: 'primary' },
        { name: 'Online Payment', type: "Online Payment", id: 51, completed: true, color: 'primary' },
      ]
    };

    return paymentmethod;
  }
}