//
//  ServerClass.swift
//  Pando Car
//
//  Created by Techno Exponent -03 on 04/04/18.
//  Copyright © 2018 TWebExponent. All rights reserved.
//

import Foundation
import UIKit
import Alamofire
import SwiftyJSON
import SVProgressHUD
import NVActivityIndicatorView
class Connectivity {
    
    class func isConnectedToInternet() ->Bool {
        return NetworkReachabilityManager()!.isReachable
    }
}

func postMethodImageUploadReturnDictionary(apiName:String,imageName:String,vc:UIViewController,imageData:UIImage,onSuccess success:@escaping (_ response: NSDictionary) ->Void) {
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    //    SVProgressHUD.show()
    //    UIApplication.shared.beginIgnoringInteractionEvents()
    
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    
    let accessToken = UserDefaults.standard.value(forKey: "api_token")
    print("UserDict: == \(accessToken!)")
    let parameters = [
        "api_token": "\(accessToken!)"
    ]
    
    let myUrl = URL(string: baseUrl+apiName);
    var request = URLRequest(url:myUrl!)
    request.httpMethod = "POST"
    let imagedata = imageData.jpegData(compressionQuality: 0.75)!
    Alamofire.upload(multipartFormData: { multipartFormData in
        multipartFormData.append(imagedata, withName: imageName, fileName: "profilePicture", mimeType: "image/jpeg")
        for (key, value) in parameters {
            multipartFormData.append(value.data(using: String.Encoding.utf8)!, withName: key)
        }
    }, to: myUrl!, method: .post,
       encodingCompletion: { encodingResult in
        switch encodingResult {
        case .success(let upload, _, _):
            upload.uploadProgress(closure: { (progress) in
                print("Upload Progress: \(progress.fractionCompleted)")
            })
            
            upload.responseJSON { response in
                guard let json = response.result.value as? [String: Any] else {
                    print("didn't get todo object as JSON from API")
                    //print("Error: \(response.result.error as! NSString)")
                    
                    return
                }
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                print("JSON: \(json)")
                success(json as NSDictionary)
            }
        case .failure(let encodingError):
            //            SVProgressHUD.dismiss()
            //            UIApplication.shared.endIgnoringInteractionEvents()
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            print("error:\(encodingError)")
            
        }
    })
}
func postMethodImageUploadPropertyWithParamReturnDict(apiName:String,property_id:String,imageName:String,vc:UIViewController,imageData:UIImage,onSuccess success:@escaping (_ response: NSDictionary) ->Void) {
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    
    let userData = UserDefaults.standard.object(forKey: "key_accessToken_info")
    let accesstoken = NSKeyedUnarchiver.unarchiveObject(with: userData as! Data) as! String
    print("api_token: == \(accesstoken)")
    print(apiName)
    let parameters = [
        "api_token": "\(accesstoken)",
        "property_id":"\(property_id)"
    ]
    print(parameters)
    let myUrl = URL(string: baseUrl+apiName);
    var request = URLRequest(url:myUrl!)
    request.httpMethod = "POST"
    //    SVProgressHUD.show()
    //    UIApplication.shared.beginIgnoringInteractionEvents()
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    
    let imagedata = imageData.jpegData(compressionQuality: 0.75)!
    Alamofire.upload(multipartFormData: { multipartFormData in
        multipartFormData.append(imagedata, withName: imageName, fileName: "profilePicture.jpeg", mimeType: "image/jpeg")
        for (key, value) in parameters {
            multipartFormData.append(value.data(using: String.Encoding.utf8)!, withName: key)
        }
    }, to: myUrl!, method: .post,
       encodingCompletion: { encodingResult in
        switch encodingResult {
        case .success(let upload, _, _):
            upload.uploadProgress(closure: { (progress) in
                print("Upload Progress: \(progress.fractionCompleted)")
            })
            
            upload.responseJSON { response in
                guard let json = response.result.value as? [String: Any] else {
                    print("didn't get todo object as JSON from API")
                    //print("Error: \(response.result.error as! NSString)")
                    return
                }
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                print("JSON: \(json)")
                success(json as NSDictionary)
            }
        case .failure(let encodingError):
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("error:\(encodingError)")
            
            
        }
    })
}

func postMethodWithImageWithParaReturnJSON(apiName: String, imgParam: String, params: [String: Any], vc: UIViewController, imageData: UIImage, onsuccess success:@escaping (_ response:JSON) -> Void){
    
    guard Connectivity.isConnectedToInternet() else {
        print("Yes! internet is available.")
        createalert(title: "Error", message: "Internet Unavailable", vc: vc)
        return
    }
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    print("Imagekey-------->>>\(imageData)")
    
    let url = baseUrl + apiName
    print(url)
    //     let imgData = imageData.pngData()
    let imgData = imageData.jpegData(compressionQuality: 1.0)
    
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    Alamofire.upload(multipartFormData: { (multipartFormData) in
        for (key, value) in params {
            multipartFormData.append("\(value)".data(using: String.Encoding.utf8)!, withName: key as String)
        }
        
        if let data = imgData{
            multipartFormData.append(data, withName: "image", fileName: "image.png", mimeType: "image/png")
            print(data)
        }
    }, usingThreshold: UInt64.init(), to: url, method: .post) { (result) in
        switch result{
        case .success(let upload, _, _):
            upload.responseJSON { response in
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                let respon = response.result.value
                //if response.error != nil{
                if let err = response.error{
                    print(err.localizedDescription)
                    return
                }
                
                print("Success %@",response)
                let json = JSON(respon!)
                success(json)
                //HUD.flash(.success)
            }
        case .failure(let error):
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("Error in upload: \(error.localizedDescription)")
        }
    }
}
func postMethowWithImage(apiName: String, imgParam: String, params: [String: Any], vc: UIViewController, imageData: UIImage, onsuccess success:@escaping (_ response:JSON) -> Void){
    
    guard Connectivity.isConnectedToInternet() else {
        print("Yes! internet is available.")
        //        alertMessage(tit: "Error", mess: "Internet Unavailable", vc: vc)
        return
    }
    
    //    sdLoader.startAnimating(atView: appDelegate.window!)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    print("Imagekey-------->>>\(imageData)")
    
    let url = baseUrl + apiName
    print(url)
    let auth = UserDefaults.standard.value(forKey: "access_token") as! String
    print(auth)
    let headers: HTTPHeaders = ["Content-type": "multipart/form-data",
                                "Authorization": "Bearer \(auth)"]
    print(headers)
    let imgData = imageData.pngData()
    
    Alamofire.upload(multipartFormData: { (multipartFormData) in
        for (key, value) in params {
            multipartFormData.append("\(value)".data(using: String.Encoding.utf8)!, withName: key as String)
        }
        if let data = imgData {
            multipartFormData.append(imgData!, withName: imgParam, fileName: "storage.png", mimeType: "image/png")
            print(data)
        }
    }, usingThreshold: UInt64.init(), to: url, method: .post , headers: headers) { (result) in
        
        switch result{
        case .success(let upload, _, _):
            upload.responseJSON { response in
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                let respon = response.result.value
                if let err = response.error{
                    print(err.localizedDescription)
                    
                    return
                }
                print("Success %@",response)
                let json = JSON(respon!)
                success(json)
                
            }
        case .failure(let error):
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("Error in upload: \(error.localizedDescription)")
        }
    }
}
func getMethodReturnJson(apiName: String, vc: UIViewController, onsuccess success:@escaping (_ response: JSON) ->Void) {
    guard Connectivity.isConnectedToInternet() else {
        print("Yes! internet is available.")
        return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    print(apiName)
    let fullUrl = baseUrl + apiName
    print(fullUrl)
    Alamofire.request(fullUrl, encoding: JSONEncoding.default).responseJSON { response in
        print(response)
        DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
            NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
        
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
        }
    }
}
func getMethodReturnWithoutJson(apiName: String, onsuccess success:@escaping (_ response: JSON) ->Void) {
    guard Connectivity.isConnectedToInternet() else {
        print("Yes! internet is available.")
        return
    }
    //   SVProgressHUD.show()
    //  UIApplication.shared.beginIgnoringInteractionEvents()
    print(apiName)
    let fullUrl = baseUrl + apiName
    print(fullUrl)
    Alamofire.request(fullUrl, encoding: JSONEncoding.default).responseJSON { response in
        print(response)
        //   SVProgressHUD.dismiss()
        //   UIApplication.shared.endIgnoringInteractionEvents()
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            //   SVProgressHUD.dismiss()
            //   UIApplication.shared.endIgnoringInteractionEvents()
            
        }
    }
}

func getMethodWithAuthorizationReturnJson(apiName: String, vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    print("Api------------ \(apiName)")
    let deviceID = "\(UIDevice.current.identifierForVendor!.uuidString)"
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json",
        "DEVICEID": "\(deviceID)"
    ]
    print(headers)
    let url = baseUrl + apiName
    
    let myUrl = URL(string: url);
    print(myUrl!)
    
    var request = URLRequest(url:myUrl!)
    request.allHTTPHeaderFields = headers
    request.httpMethod = "GET"
    
    
    Alamofire.request(request)
        .responseJSON { response in
            guard let res = response.result.value as? [String:Any] else {
                print(response.value)
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                print("didn't get todo object as JSON from API")
                return
            }
            // print("JSON:-> ApiCallForShowTrendingLeaks ===>  \(res)")
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
    }
}

func getMethodReturnData(apiName: String, vc: UIViewController, onSuccess success:@escaping (_ response: Data) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    print("Api------------ \(apiName)")
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    
    let url = baseUrl + apiName
    print(url)
    Alamofire.request(url, method: .get, parameters: nil, encoding: URLEncoding.default).responseJSON { response in
        guard let json = response.data else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("didn't get todo object as JSON from API")
            return
        }
        print("JSON:-> ApiCallForShowTrendingLeaks ===>  \(json)")
        
        success(json as Data)
        DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
            NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
        
    }
}

func getMethodWithAuthorizationReturnData(apiName: String, vc: UIViewController, onSuccess success:@escaping (_ response: Data) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    print("Api------------ \(apiName)")
    let auth = UserDefaults.standard.value(forKey: "access_token") as! String
    print(auth)
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = [
        "Authorization": "Bearer \(auth)",
        "Content-Type": "application/json"
    ]
    print(headers)
    
    let myUrl = URL(string: baseUrl + apiName)
    print(myUrl!)
    var request = URLRequest(url:myUrl!)
    request.httpMethod = "GET"
    
    request.allHTTPHeaderFields = headers
    Alamofire.request(request)
        .responseJSON { response in
            guard let json = response.data else {
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                print("didn't get todo object as JSON from API")
                return
            }
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("JSON:-> ApiCallForShowTrendingLeaks ===>  \(json)")
            success(json as Data)
    }
}

func postMethodReturnData(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: Data) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url =   apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let json = response.data {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            //let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func postMethodReturnWithAuthorizationData(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: Data) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    
    let auth = UserDefaults.standard.value(forKey: "access_token") as! String
    print(auth)
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = [
        "Authorization": "Bearer \(auth)",
        "Content-Type": "application/json"
    ]
    print(headers)
    
    
    
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.data {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            success(res)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func postMethodReturnJsonTest(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let url =  apiName
    print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}



func postMethodReturnJson(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodReturnJsonLogin(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    
    let url =  baseUrl + apiName
  //  print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    var deviceId : String
    deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
    let headers: HTTPHeaders = [
        "DEVICEID": "\(deviceId)" ,
        "Content-Type": "application/json"
    ]
    print(headers)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodImageUpload(apiName:String,imageName:String,vc:UIViewController,imageData:UIImage,onSuccess success:@escaping (_ response: NSDictionary) ->Void) {
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    
    let url = baseUrl + apiName
    print("Api------------ \(url)")
    let myUrl = URL(string: url)
    var request = URLRequest(url:myUrl!)
    request.httpMethod = "POST"
    let auth = UserDefaults.standard.value(forKey: "access_token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "Authorization": "Bearer \(auth)",
        "Content-Type": "multipart/form-data"
    ]
    print(headers)
    request.allHTTPHeaderFields = headers
    //    request.httpBody = params.data(using: String.Encoding.utf8);
    let imagedata = imageData.jpegData(compressionQuality: 0.75)!
    Alamofire.upload(multipartFormData: { multipartFormData in
        multipartFormData.append(imagedata, withName: imageName, fileName: "image", mimeType: "image/jpeg")
    }, to: myUrl!, method: .post,
       encodingCompletion: { encodingResult in
        switch encodingResult {
        case .success(let upload, _, _):
            upload.uploadProgress(closure: { (progress) in
                print("Upload Progress: \(progress.fractionCompleted)")
            })
            
            upload.responseJSON { response in
                guard let json = response.result.value as? [String: Any] else {
                    print("didn't get todo object as JSON from API")
                    //print("Error: \(response.result.error as! NSString)")
                    
                    return
                }
                print("JSON: \(json)")
                success(json as NSDictionary)
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            }
        case .failure(let encodingError):
            print("error:\(encodingError)")
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
        }
    })
}
func postMethodReturnWithAuthorizationJson(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json"
    ]
    print(headers)
    
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodSocialSignIn(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    
    
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url = baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    var deviceId : String
    deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
    let headers: HTTPHeaders = [
        "DEVICEID": "\(deviceId)" ,
        "Content-Type": "application/json"
    ]
    print(headers)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        // DismissSVProgressHUD()
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            //HUD.flash(.error)
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func postMethodSocialSignInApple(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    
    
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url = baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    var deviceId : String
    deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
    let headers: HTTPHeaders = [
        "DEVICEID": "\(deviceId)" ,
        "Content-Type": "application/json",
        "WID": "1"
    ]
    print(headers)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        // DismissSVProgressHUD()
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            //HUD.flash(.error)
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func requestWith(endUrl: String, imageData: Data?, parameters: [String : Any], onCompletion: ((JSON?) -> Void)? = nil, onError: ((Error?) -> Void)? = nil){
    //    SVProgressHUD.show()
    ////    UIApplication.shared.beginIgnoringInteractionEvents()
    let url = baseUrl + endUrl
    
    let headers: HTTPHeaders = [
        "Content-type": "multipart/form-data"
    ]
    print(url)
    print(parameters)
    
    Alamofire.upload(multipartFormData: { (multipartFormData) in
        for (key, value) in parameters {
            multipartFormData.append("\(value)".data(using: String.Encoding.utf8)!, withName: key as String)
        }
        
        if let data = imageData{
            multipartFormData.append(data, withName: "image", fileName: "image.png", mimeType: "image/png")
        }
        
    }, usingThreshold: UInt64.init(), to: url, method: .post, headers: headers) { (result) in
        switch result{
            
        case .success(let upload, _, _):
            upload.responseJSON { response in
                print("Succesfully uploaded")
                if let err = response.error{
                    onError?(err)
                    return
                }
                let json = JSON(response.value!)
                onCompletion?(json)
            }
        case .failure(let error):
            //            SVProgressHUD.dismiss()
            //            UIApplication.shared.endIgnoringInteractionEvents()
            print("Error in upload: \(error.localizedDescription)")
            onError?(error)
        }
    }
}
func putMethod(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json"
    ]
    print(headers)
    let url = baseUrl + apiName
    print(url)
    
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .put, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        
        print("Response---->>>%@",response.result)
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
        }
        else {
            
            let err = response.result.error
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func requestWithPut(methodName:String, parameter:[String:Any], successHandler: @escaping(_ success:JSON) -> Void)
{
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let parameters: Parameters = parameter
    var jsonResponse:JSON!
    var errorF:NSError!
    //        print(errorF)
    let urlString = baseUrl.appending("\(methodName)")
    print("parameters",parameters)
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "Authorization": "Token \(auth)"
    ]
    let configuration = URLSessionConfiguration.default
    configuration.timeoutIntervalForRequest = 120
    let sessionManager = Alamofire.SessionManager(configuration: configuration)
    
    print(urlString)
    print(headers)
    sessionManager.request(urlString, method: .put, parameters: parameters, encoding:JSONEncoding.default , headers: headers).responseJSON { (response:DataResponse<Any>) in
        switch response.result{
        case .failure(let error):
            print(error.localizedDescription)
            errorF = error as NSError
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
            break
        case .success(let value):
            print("value",value)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            do{
                let json = try JSON(data: response.data!)
                let jsonType = json as JSON
                print("jsonType",jsonType)
                jsonResponse = jsonType
                break
            }
            catch{
                print("error",error.localizedDescription)
            }
            
        }
        if jsonResponse !=  nil{
            successHandler(jsonResponse)
        }
            
            
        else{
        }
        // KRProgressHUD.dismiss()
        //        SVProgressHUD.dismiss()
        //        sessionManager.session.invalidateAndCancel()
    }
}
func requestWithPutWithCustomHeader(methodName:String, parameter:[String:Any],header: [String:Any], successHandler: @escaping(_ success:JSON) -> Void)
{
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let parameters: Parameters = parameter
    var jsonResponse:JSON!
    var errorF:NSError!
    //        print(errorF)
    let urlString = baseUrl.appending("\(methodName)")
    print("parameters",parameters)
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = header as! HTTPHeaders
    let configuration = URLSessionConfiguration.default
    configuration.timeoutIntervalForRequest = 120
    let sessionManager = Alamofire.SessionManager(configuration: configuration)
    print(urlString)
    sessionManager.request(urlString, method: .put, parameters: parameters, encoding:JSONEncoding.default , headers: headers).responseJSON { (response:DataResponse<Any>) in
        switch response.result{
        case .failure(let error):
            print(error.localizedDescription)
            errorF = error as NSError
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
            break
        case .success(let value):
            print("value",value)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            do{
                let json = try JSON(data: response.data!)
                let jsonType = json as JSON
                print("jsonType",jsonType)
                jsonResponse = jsonType
                break
            }
            catch{
                print("error",error.localizedDescription)
            }
            
        }
        if jsonResponse !=  nil{
            successHandler(jsonResponse)
        }
            
            
        else{
        }
        // KRProgressHUD.dismiss()
        //        SVProgressHUD.dismiss()
        //        sessionManager.session.invalidateAndCancel()
    }
}
func postMethodHomePage(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let baseUrl = "http://192.168.0.66:8001/api/front/v1/"
    let url = baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
        }
        else {
            let err = response.result.error
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodQuery(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url = baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
        }
        else {
            let err = response.result.error
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodQueryWithoutVc(apiName: String, params: [String: Any], onSuccess success:@escaping (_ response: JSON) ->Void) {
    var auth1 = String()
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            //  createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url = baseUrl + apiName
    print(url)
    let headers: HTTPHeaders
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    if UserDefaults.standard.value(forKey: "is-login") != nil {
        var deviceId : String
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        auth1 = UserDefaults.standard.value(forKey: "token") as! String
        print(auth1)
        headers = [
            "Content-Type": "application/json",
            "Authorization": "Token \(auth1)",
            "WAREHOUSE": "\(wareHouseId)",
            "DEVICEID": "\(deviceId)" ,
        ]
    }
    else {
        var deviceId : String
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        headers = [
            "Content-Type": "application/json",
            "WAREHOUSE": "\(wareHouseId)",
            "DEVICEID": "\(deviceId)" ,
        ]
    }
    print(headers)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
        }
    }
}
func postMethodQueryWithVc(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    var auth1 = String()
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    vc.view.isUserInteractionEnabled = false
    let url = baseUrl + apiName
    print(url)
    let headers: HTTPHeaders
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    if UserDefaults.standard.value(forKey: "is-login") != nil {
        var deviceId : String
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        auth1 = UserDefaults.standard.value(forKey: "token") as! String
        print(auth1)
        headers = [
            "Content-Type": "application/json",
            "Authorization": "Token \(auth1)",
            "WAREHOUSE": "\(wareHouseId)",
            "DEVICEID": "\(deviceId)" ,
        ]
    }
    else {
        var deviceId : String
        deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
        headers = [
            "Content-Type": "application/json",
            "WAREHOUSE": "\(wareHouseId)",
            "DEVICEID": "\(deviceId)" ,
        ]
    }
    
    
    print(headers)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            vc.view.isUserInteractionEnabled = true
            let json = JSON(res)
            success(json)
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            vc.view.isUserInteractionEnabled = true
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
        }
    }
}
func postMethodQuery1(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url = apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
        }
    }
}
func postMethodQuery2(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth1 = UserDefaults.standard.value(forKey: "token") as! String
    print(auth1)
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "Authorization": "Token \(auth1)"]
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func postMethodQueryWithoutAuthorization(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        //        "Authorization": "Token \(auth1)"
    ]
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}


func getMethodWithAuthorizationWithCustomHeaderReturnJson(apiName: String, vc: UIViewController,header: [String:Any],isDismiss:Bool = true, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = header as! HTTPHeaders
    print(headers)
    let url = baseUrl + apiName
    
    let myUrl = URL(string: url);
    print(myUrl!)
    var request = URLRequest(url:myUrl!)
    request.httpMethod = "GET"
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
    NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    request.allHTTPHeaderFields = headers
    Alamofire.request(request)
        .responseJSON { response in
            let statusCode = response.response?.statusCode
            // UIApplication.shared.endIgnoringInteractionEvents()
            if isDismiss == true {
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                //UIApplication.shared.endIgnoringInteractionEvents()
            }
            if statusCode == 200 {
                guard let res = response.result.value as? [String:Any] else {
                    return
                }
                let json = JSON(res)
                success(json)
            }
            else {
                var js = JSON()
                js["status"] = 999
                success(js)
                print("didn't get todo object as JSON from API")
            }
    }
}

func getMethodWithAuthorizationWithCustomHeaderReturnJsonViewCart(apiName: String, vc: UIViewController,header: [String:Any],isDismiss:Bool = true,loaderShow:Bool = true, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = header as! HTTPHeaders
    print(headers)
    let url = baseUrl + apiName
    
    let myUrl = URL(string: url);
    print(myUrl!)
    var request = URLRequest(url:myUrl!)
    request.httpMethod = "GET"
    if loaderShow == true {
        let activityData = ActivityData()
         NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
         DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
             NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    }
    request.allHTTPHeaderFields = headers
    Alamofire.request(request)
        .responseJSON { response in
            let statusCode = response.response?.statusCode
            // print(statusCode)
            UIApplication.shared.endIgnoringInteractionEvents()
            if loaderShow == true {
                if isDismiss == true {
                    
                    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                        NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                    // UIApplication.shared.endIgnoringInteractionEvents()
                }
            }
            if statusCode == 200 {
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                guard let res = response.result.value as? [String:Any] else {
                    return
                }
                let json = JSON(res)
                success(json)
            }
            else {
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                var js = JSON()
                js["status"] = 999
                success(js)
                print("didn't get todo object as JSON from API")
            }
    }
}
func postMethodQueryWithAuthorization(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url =  baseUrl + apiName
    print(url)
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "Authorization": "Token \(auth)"
    ]
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
        }
        else {
            let err = response.result.error
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func getMethodWithAuthorizationReturnJsonWithoutDeviceId(apiName: String, vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json",
    ]
    print(headers)
    let url = baseUrl + apiName
    
    let myUrl = URL(string: url);
    print(myUrl!)
    
    var request = URLRequest(url:myUrl!)
    request.allHTTPHeaderFields = headers
    request.httpMethod = "GET"
    
    
    Alamofire.request(request)
        .responseJSON { response in
            guard let res = response.result.value as? [String:Any] else {
                print("didn't get todo object as JSON from API")
                //                print(response.value)
                var js = JSON()
                js["status"] = 999
                success(js)
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                
                return
            }
            // print("JSON:-> ApiCallForShowTrendingLeaks ===>  \(res)")
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
    }
}

func putMethodReturnJson(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json",
    ]
    print(headers)
    Alamofire.request(url, method: .put, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
        }
        else {
            
            let err = response.result.error
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodQueryToBookOrder(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url =  apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            SVProgressHUD.dismiss()
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func getMethodWithAuthorizationReturnJsonwithWareHouseId(apiName: String, vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json",
        "WID": "1",
    ]
    print(headers)
    let url = baseUrl + apiName
    
    let myUrl = URL(string: url);
    print(myUrl!)
    
    var request = URLRequest(url:myUrl!)
    request.allHTTPHeaderFields = headers
    request.httpMethod = "GET"
    
    
    Alamofire.request(request)
        .responseJSON { response in
            guard let res = response.result.value as? [String:Any] else {
                print(response.value)
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                print("didn't get todo object as JSON from API")
                return
            }
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
    }
}
func getMethodWithAuthorizationReturnJsonForSearchFilter(apiName: String, vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    print("Api------------ \(apiName)")
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "WAREHOUSE" : "\(wareHouseId)"
    ]
    print(headers)
    let url = baseUrl + apiName
    
    let myUrl = URL(string: url);
    print(myUrl!)
    
    var request = URLRequest(url:myUrl!)
    request.allHTTPHeaderFields = headers
    request.httpMethod = "GET"
    
    
    Alamofire.request(request)
        .responseJSON { response in
            if let res = response.result.value {
                let json = JSON(res)
                success(json)
                DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                    NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
                
            }
    }
}
func postMethodReturnJsonforCategory(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func requestWithPutToBook(methodName:String, parameter:[String:Any], vc: UIViewController, successHandler: @escaping(_ success:JSON) -> Void)
{
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let parameters: Parameters = parameter
    var jsonResponse:JSON!
    var errorF:NSError!
    let urlString = baseUrl.appending("\(methodName)")
    print("parameters",parameters)
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "Authorization": "Token \(auth)"
    ]
    let configuration = URLSessionConfiguration.default
    configuration.timeoutIntervalForRequest = 120
    let sessionManager = Alamofire.SessionManager(configuration: configuration)
    
    print(urlString)
    print(headers)
    sessionManager.request(urlString, method: .put, parameters: parameters, encoding:JSONEncoding.default , headers: headers).responseJSON { (response:DataResponse<Any>) in
        switch response.result{
        case .failure(let error):
            print(error.localizedDescription)
            errorF = error as NSError
            break
        case .success(let value):
            print("value",value)
            do{
                let json = try JSON(data: response.data!)
                print("json",json)
                let jsonType = json as JSON
                print("jsonType",jsonType)
                jsonResponse = jsonType
                break
            }
            catch{
                print("error",error.localizedDescription)
            }
        }
        if jsonResponse !=  nil{
            successHandler(jsonResponse)
        }
        else{
        }
        DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
            NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
        
    }
}
func postMethodSignup(apiName: String, params: NSDictionary, vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(url)")
    print("Params-------- %@",params)
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
    let headers: HTTPHeaders = [
        "DEVICEID": "\(deviceId)",
        "Content-Type": "application/json"
    ]
    print(headers)
    Alamofire.request(url, method: .post, parameters: params as? Parameters,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodQueryApplyCoupon(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth1 = UserDefaults.standard.value(forKey: "token") as! String
    print(auth1)
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "Authorization": "Token \(auth1)" ,
        "WAREHOUSE" : "\(wareHouseId)"]
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
      print("Headers-------- %@",headers)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        //  DismissSVProgressHUD()
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func deleteMethod(apiName: String,  vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json"
    ]
    print(headers)
    let url = baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    
    Alamofire.request(url, method: .delete,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response.result)
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            
        }
        else {
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func postMethodCustomHeader(apiName: String, params: [String: Any], vc: UIViewController, header: [String:Any], onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let headers: HTTPHeaders = header as! HTTPHeaders
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            // SVProgressHUD.dismiss()
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
        }
    }
}
func postMethodQuerySave(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth1 = UserDefaults.standard.value(forKey: "token") as! String
    print(auth1)
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "Authorization": "Token \(auth1)",
        "WAREHOUSE": "\(wareHouseId)"]
    let url =  baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .post, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}
func requestWithPutForEditAddress(methodName:String, parameter:[String:Any], successHandler: @escaping(_ success:JSON) -> Void)
{
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let parameters: Parameters = parameter
    var jsonResponse:JSON!
    var errorF:NSError!
    //        print(errorF)
    let urlString = baseUrl.appending("\(methodName)")
    print("parameters",parameters)
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    let headers: HTTPHeaders = [
        "Content-Type": "application/json",
        "Authorization": "Token \(auth)",
        "WAREHOUSE": "\(wareHouseId)"
    ]
    let configuration = URLSessionConfiguration.default
    configuration.timeoutIntervalForRequest = 120
    let sessionManager = Alamofire.SessionManager(configuration: configuration)
    
    print(urlString)
    print(headers)
    sessionManager.request(urlString, method: .put, parameters: parameters, encoding:JSONEncoding.default , headers: headers).responseJSON { (response:DataResponse<Any>) in
        switch response.result{
        case .failure(let error):
            print(error.localizedDescription)
            errorF = error as NSError
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            break
        case .success(let value):
            print("value",value)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            do{
                let json = try JSON(data: response.data!)
                let jsonType = json as JSON
                print("jsonType",jsonType)
                jsonResponse = jsonType
                break
            }
            catch{
                print("error",error.localizedDescription)
            }
            
        }
        if jsonResponse !=  nil{
            successHandler(jsonResponse)
        }
            
            
        else{
        }
        // KRProgressHUD.dismiss()
        //        SVProgressHUD.dismiss()
        //        sessionManager.session.invalidateAndCancel()
    }
}
func putMethodEdit(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    let headers: HTTPHeaders = [
        "Authorization": "Token \(auth)",
        "Content-Type": "application/json",
        "WAREHOUSE": "\(wareHouseId)"
    ]
    print(headers)
    let url = baseUrl + apiName
    print(url)
    
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    Alamofire.request(url, method: .put, parameters: params,encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        
        print("Response---->>>%@",response.result)
        if let res = response.result.value {
            let json = JSON(res)
            success(json)
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
        }
        else {
            
            let err = response.result.error
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}


func callMenuWebService(url: String, imageData: Data?, parameters: [String : Any]){
    let headers: HTTPHeaders = [
        /* "Authorization": "your_access_token",  in case you need authorization header */
        "Content-type": "multipart/form-data"
    ]
    Alamofire.upload(multipartFormData: { (multipartFormData) in
        for (key, value) in parameters {
            multipartFormData.append("\(value)".data(using: String.Encoding.utf8)!, withName: key as String)
        }
        
        if let data = imageData{
            multipartFormData.append(data, withName: "image", fileName: "image.png", mimeType: "image/png")
        }
        
    }, usingThreshold: UInt64.init(), to: url, method: .post, headers: headers) { (result) in
        switch result{
            
        case .success(let upload, _, _):
            upload.responseJSON { response in
                print(response)
                if let result = response.result.value {
                    let jsonResult = result as? NSDictionary
                    if let result = jsonResult  {
                        let status  = result .value(forKey: "status") as? Int ?? 0
                        
                        if status == 1 {
                            let resData = response.data!
                            UserDefaults.standard.set(resData, forKey: "menudata")
                            UserDefaults.standard.synchronize()
                            
                        } else {
                            
                        }
                    }
                    
                }
                
            }
        case .failure(let error):
            
            print("Error in upload: \(error.localizedDescription)")
            
        }
    }
    
    
}
func postMethodRegisterDevice(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    
    
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url = baseUrl + apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    var deviceId : String
    deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    print(auth)
    let headers: HTTPHeaders = [
        "DEVICEID": "\(deviceId)" ,
        "Content-Type": "application/json",
        "Authorization": "Token \(auth)"
    ]
    print(headers)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        // DismissSVProgressHUD()
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            //HUD.flash(.error)
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

func postMethodSubstitute(apiName: String, params: [String: Any], vc: UIViewController, onSuccess success:@escaping (_ response: JSON) ->Void) {
    
    guard Connectivity.isConnectedToInternet()
        else {
            print("Yes! internet is available.")
            createalert(title: "Alert", message: "Internet Unavailable", vc: vc)
            return
    }
    
    
    let activityData = ActivityData()
    NVActivityIndicatorView.DEFAULT_TYPE = .ballPulse
    DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
        NVActivityIndicatorPresenter.sharedInstance.startAnimating(activityData,nil)}
    let url = apiName
    print(url)
    print("Api------------ \(apiName)")
    print("Params-------- %@",params)
    var deviceId : String
    deviceId = "\(UIDevice.current.identifierForVendor!.uuidString)"
    let auth = UserDefaults.standard.value(forKey: "token") as! String
    let headers: HTTPHeaders = [
        "DEVICEID": "\(deviceId)" ,
        "Content-Type": "application/json",
        "Authorization": "Token \(auth)"
    ]
    print(headers)
    Alamofire.request(url, method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers).responseJSON { (response: DataResponse<Any>) in
        // DismissSVProgressHUD()
        print("Response---->>>%@",response)
        if let res = response.result.value {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            let json = JSON(res)
            success(json)
        }
        else {
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now()) {
                NVActivityIndicatorPresenter.sharedInstance.stopAnimating(nil)}
            
            //HUD.flash(.error)
            let err = response.result.error
            print("ServerError------>>>>>>",err!)
            createalert(title: "Alert", message: "Server Error Please Try After Sometime", vc: vc)
        }
    }
}

