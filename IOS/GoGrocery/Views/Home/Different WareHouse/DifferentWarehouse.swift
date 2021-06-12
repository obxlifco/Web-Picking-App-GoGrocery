//
//  DifferentWarehouse.swift
//  GoGrocery
//
//  Created by Nav63 on 13/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class DifferentWarehouse: UIView {

    @IBOutlet weak var viewWareHouse: UIView!
    @IBOutlet weak var btnNo: UIButton!
    @IBOutlet weak var btnYes: UIButton!
    
}
var wareHouseXib = DifferentWarehouse()
func requestWareHouseView(vc: UIViewController){
    
    wareHouseXib.removeFromSuperview() // make it only once
    wareHouseXib = Bundle.main.loadNibNamed("DifferentWareHouse", owner: vc, options: nil)?.first as! DifferentWarehouse
    wareHouseXib.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    wareHouseXib.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        wareHouseXib.alpha = 1
    }
    appdelegate.window?.addSubview(wareHouseXib)
}

