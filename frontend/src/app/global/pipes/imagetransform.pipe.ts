import { Pipe, PipeTransform } from '@angular/core';
import {GlobalVariable} from '../../global/service/global';
@Pipe({
  name: 'imagetransform'
})
export class ImagetransformPipe implements PipeTransform {
  	public s3Url = GlobalVariable.S3_URL;
	/**
	   * Method for finding cover image from array
	   * send full link of s3 url
	   * @parma value array
	*/
  	transform(value: any, args?: any): any {
       
		let formedImageUrl = '/assets/images/noimg.png';
		let imageType = args[2];
		let imageFor  = args[0];
		let imageSize = args[1];
	
		let imageSizeArray:Object = {
			'200' : '200x200',
			'400' : '400x400',
			'800' : '800x800'
		}
		if(value instanceof Array && imageType == 'cover') {
			let findCoverImage = value.filter(imageObject => {
				if(imageObject['is_cover'] == 1) {
					return imageObject;
				}
			});
			
			if(findCoverImage.length > 0) {
				formedImageUrl = this.s3Url+imageFor+'/'+imageSizeArray[imageSize]+'/'+findCoverImage[0]['img'];
			} else {
				formedImageUrl = '/assets/images/noimg.png';
			}
		} else if(value instanceof Object && imageType == 'cover') {
			formedImageUrl = value && value['is_cover'] && value['is_cover'] == 1 ? this.s3Url+imageFor+'/'+imageSizeArray[imageSize]+'/'+value['img'] : '/assets/images/noimg.png';

		}
		
		return formedImageUrl;
	}
	
}