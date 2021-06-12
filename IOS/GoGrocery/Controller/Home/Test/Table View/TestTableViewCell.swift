//
//  TestTableViewCell.swift
//  GoGrocery
//
//  Created by NAV63 on 25/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class TestTableViewCell: UITableViewCell {
  @IBOutlet weak var testCollectionView: UICollectionView!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
