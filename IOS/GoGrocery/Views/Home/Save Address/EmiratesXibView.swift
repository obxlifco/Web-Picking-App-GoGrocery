//
//  EmiratesXibView.swift
//  GoGrocery
//
//  Created by BMS-09-M on 29/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class EmiratesXibView: UIView {

    @IBOutlet weak var lblAbuDhabi: UILabel!
    @IBOutlet weak var btnAbuDhabi: UIButton!
    @IBOutlet weak var lblDubai: UILabel!
    @IBOutlet weak var btnDubai: UIButton!
    @IBOutlet weak var lblAjman: UILabel!
    @IBOutlet weak var btnAjman: UIButton!
    
    @IBOutlet weak var lblSharjah: UILabel!
    @IBOutlet weak var btnSarjah: UIButton!
    @IBOutlet weak var lblFujairah: UILabel!
    @IBOutlet weak var btnFujairah: UIButton!
    @IBOutlet weak var lblRAsAl: UILabel!
    @IBOutlet weak var btnRasAl: UIButton!
    
}
var LocationXib = EmiratesXibView()
func requestLocationViewGlobal(vc: UIViewController){
    
    LocationXib.removeFromSuperview() // make it only once
    LocationXib = Bundle.main.loadNibNamed("EmiratesView", owner: vc, options: nil)?.first as! EmiratesXibView
    LocationXib.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    LocationXib.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        LocationXib.alpha = 1
    }
    appdelegate.window?.addSubview(LocationXib)
}
