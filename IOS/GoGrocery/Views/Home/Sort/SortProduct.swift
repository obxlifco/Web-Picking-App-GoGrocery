//
//  SortProduct.swift
//  GoGrocery
//
//  Created by BMS-09-M on 11/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class SortProduct: UIView {
    @IBOutlet weak var btnPopularity: UIButton!
    @IBOutlet weak var lblPopularity: UILabel!
    @IBOutlet weak var btnNewArrival: UIButton!
    
    
    @IBOutlet weak var btnPriceHighToLow: UIButton!
    @IBOutlet weak var lblPriceHighToLow: UILabel!
    @IBOutlet weak var btnPriceHighToLowFull: UIButton!
    
    @IBOutlet weak var btnPriceLowToHigh: UIButton!
    @IBOutlet weak var lblPriceLowToHigh: UILabel!
    @IBOutlet weak var priceLowToHighFull: UIButton!
    
    @IBOutlet weak var btnCancel: UIButton!
    @IBOutlet weak var btnApply: UIButton!
    @IBOutlet weak var sortView: UIView!
    
    
}

var sortXib = SortProduct()
func requestsortView(vc: UIViewController){
    
    sortXib.removeFromSuperview() // make it only once
    sortXib = Bundle.main.loadNibNamed("SortProduct", owner: vc, options: nil)?.first as! SortProduct
    sortXib.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    sortXib.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        sortXib.alpha = 1
    }
    appdelegate.window?.addSubview(sortXib)
}
