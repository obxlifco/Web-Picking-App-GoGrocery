//
//  CategoryViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 16/09/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import SwiftyJSON
class CategoryViewController: UIViewController ,UICollectionViewDelegate, UICollectionViewDataSource, UICollectionViewDelegateFlowLayout{
    
    @IBOutlet weak var navigationView: UIView!
    @IBOutlet weak var collectionView: UICollectionView!
    private let spacing:CGFloat = 8
    var lat = String()
    var long = String()
    var dataArray = [JSON]()
    var screenSize: CGRect!
    var screenWidth: CGFloat!
    var screenHeight: CGFloat!
    var selectedIndex  = Int()
    var catlat = String()
    var catlong = String()
    override func viewDidLoad() {
        super.viewDidLoad()

        screenSize = UIScreen.main.bounds
        screenWidth = screenSize.width
        screenHeight = screenSize.height
        navigationView.addShadow1()
        let layout: UICollectionViewFlowLayout = UICollectionViewFlowLayout()
        layout.sectionInset = UIEdgeInsets(top: 0, left: 0, bottom: 0, right: 0)
        layout.itemSize = CGSize(width: screenWidth/2, height: screenWidth/2)
        layout.minimumInteritemSpacing = 15
        layout.minimumLineSpacing = 15
        collectionView!.collectionViewLayout = layout
//        collectionView.delegate = self
//        collectionView.dataSource = self
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        let backButton = UIBarButtonItem()
        backButton.title = ""
        navigationController?.navigationBar.topItem?.backBarButtonItem = backButton
        self.navigationController?.isNavigationBarHidden = true
        self.ApiCallToGetCat()
    }
    @IBAction func btnBackAction(_ sender: Any) {
        let vc = storyboard?.instantiateViewController(withIdentifier: "MarkLocationViewController") as! MarkLocationViewController
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
        func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
            return dataArray.count
           //  return 15
        }
        
        func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
            let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "CategoryMainCollectionViewCell", for: indexPath) as! CategoryMainCollectionViewCell
            cell.cellView.layer.cornerRadius = 5
            cell.cellView.addShadow1()
            cell.cellView.layer.borderColor = UIColor.lightGray.cgColor
            cell.cellView.layer.borderWidth = 0.5
            let dataDict = dataArray[indexPath.row].dictionaryValue
            if  dataDict["image"]?.stringValue != nil {
                let storePic = dataDict["image"]?.stringValue
                let fullUrl = MAIN_CAT_LOGO + storePic!
                let url = URL(string: fullUrl)
                print(url!)
                cell.imgCity.sd_setImage(with: url, placeholderImage: UIImage(named: "no_image"))
            }
            cell.lblCat.text = dataDict["name"]?.stringValue
           // cell.imgCity.image = UIImage(named:"p1")
             cell.imgCity.layer.cornerRadius = 5
            return cell
        }
        
        func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        
               let dataDict = dataArray[indexPath.row].dictionaryValue
                print(dataDict)
            var id = dataDict["id"]!.intValue
            let storyboard:UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = storyboard.instantiateViewController(withIdentifier: "SelectCityViewController") as! SelectCityViewController
            vc.storeID = "\(id)"
            vc.slat = catlat
            vc.slong = catlong
            self.navigationController?.pushViewController(vc, animated: true)
        }
        func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
            let noOfCellsInRow = 1
            let flowLayout = collectionViewLayout as! UICollectionViewFlowLayout
            let totalSpace = flowLayout.sectionInset.left
                + flowLayout.sectionInset.right
                + (flowLayout.minimumInteritemSpacing * CGFloat(noOfCellsInRow - 1))
            let size = Int((collectionView.bounds.width - totalSpace) / CGFloat(noOfCellsInRow))
            return CGSize(width: size, height: 150)
        }
        func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, insetForSectionAt section: Int) -> UIEdgeInsets {
            return UIEdgeInsets.zero
        }
        
        func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
            return 8
        }
        
        func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumLineSpacingForSectionAt section: Int) -> CGFloat {
            return 8
        }
    func ApiCallToGetCat() {
        getMethodReturnJson(apiName: "get_storetype/", vc: self) { (response: JSON) in
          print(response)
            self.dataArray = response["data"].arrayValue
            if self.dataArray.count != 0 {
                self.collectionView.reloadData()
            }
        }
    }
}
/*
extension UIView {
    func addShadow1() {
        self.layer.shadowColor = UIColor.lightGray.cgColor
        self.layer.shadowOffset = CGSize(width: 0, height: 1)
        self.layer.shadowOpacity = 1
        self.layer.shadowRadius = 1.5
        self.clipsToBounds = false
    }
    func addShadowNote() {
         self.layer.shadowColor = UIColor.lightGray.cgColor
         self.layer.shadowOffset = CGSize(width: 0, height: 1)
         self.layer.shadowOpacity = 1
         self.layer.shadowRadius = 1
         self.clipsToBounds = false
     }
}
 */
