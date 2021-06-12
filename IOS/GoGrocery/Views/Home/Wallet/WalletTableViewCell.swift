//
//  WalletTableViewCell.swift
//  GoGrocery
//
//  Created by Nav63 on 11/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class WalletTableViewCell: UITableViewCell {

     @IBOutlet weak var lblDate: UILabel!
     @IBOutlet weak var lblEarnedPoints: UILabel!
     @IBOutlet weak var lblUsedPoints: UILabel!
     @IBOutlet weak var lblRemainingPoints: UILabel!
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
