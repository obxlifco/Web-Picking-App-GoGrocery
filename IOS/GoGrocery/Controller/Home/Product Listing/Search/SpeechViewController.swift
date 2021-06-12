//
//  SpeechViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 08/04/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
import Speech
import AVKit

protocol MicSelectDelegate: class {
    func MicTypeSelected(text : String)
}
class SpeechViewController: UIViewController ,SFSpeechRecognizerDelegate {

    @IBOutlet weak var btnMic: UIButton!
    @IBOutlet weak var lblText: UILabel!
    @IBOutlet weak var btnCancel: UIButton!
    weak var delegate : MicSelectDelegate?
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale.init(identifier: "en-US"))
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    var micBool = false
    var speechString = String()
    var timer = Timer()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        micBool = true
        btnMic.setTitle("STOP", for: .normal)
        self.lblText.text = ""
        CheckAuthorization()
        // Do any additional setup after loading the view.
    }
    
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
    
    @IBAction func btnCancelAction(_ sender: Any) {
          self.navigationController?.popViewController(animated: true)
    }
    
    @IBAction func btnMicAction(_ sender: Any) {
        if micBool == false {
            micBool = true
            startRecording()
            btnMic.setTitle("START", for: .normal)
        }
        else {
            micBool = false
            self.recognitionTask?.cancel()
            btnMic.setTitle("STOP", for: .normal)
        }
    }
    
    func CheckAuthorization() {
        speechRecognizer!.delegate = self
        SFSpeechRecognizer.requestAuthorization { (authStatus) in
            switch authStatus {
            case .authorized:
                self.startRecording()
                break
            case .denied:
                print("User denied access to speech recognition")
                createalert(title: "Alert", message: "Enable microphone acces to search by voice , to enable please go to setting and provide microphone access", vc: self)
            case .restricted:
                print("Speech recognition restricted on this device")
            case .notDetermined:
                print("Speech recognition not yet authorized")
            }
        }
    }
 
    func startRecording() {
        if recognitionTask != nil {
            recognitionTask?.cancel()
            recognitionTask = nil
        }
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(AVAudioSession.Category.record)
            try audioSession.setMode(AVAudioSession.Mode.measurement)
            // try audioSession.setActive(true, withFlags: .notifyOthersOnDeactivation)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("audioSession properties weren't set because of an error.")
        }
        
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        
        let inputNode = audioEngine.inputNode
        guard let recognitionRequest = recognitionRequest else {
            fatalError("Unable to create an SFSpeechAudioBufferRecognitionRequest object")
        }
        Timer.scheduledTimer(timeInterval: 2, target: self, selector: #selector(runTimedCode), userInfo: nil, repeats: false)
        recognitionRequest.shouldReportPartialResults = true
        recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest, resultHandler: { (result, error) in
            var isFinal = false
            if result != nil {
                print(result!)

                self.lblText.text = result?.bestTranscription.formattedString
                self.speechString = (result?.bestTranscription.formattedString)!
                isFinal = (result?.isFinal)!
                self.timer.invalidate()
                self.timer = Timer.scheduledTimer(timeInterval: 2, target: self, selector: #selector(self.runTimedCode), userInfo: nil, repeats: false)

            }
            if error != nil || isFinal {
                self.audioEngine.stop()
                inputNode.removeTap(onBus: 0)
                self.recognitionRequest = nil
                self.recognitionTask = nil
//                print(self.lblText.text)
//                print(result?.transcriptions)
//                  self.navigationController?.popViewController(animated: true)
//                  self.delegate?.MicTypeSelected(text : self.lblText.text!)
//                  self.recognitionTask?.cancel()
                //  self.microphoneButton.isEnabled = true
            }
        })
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { (buffer, when) in
            self.recognitionRequest?.append(buffer)
        }
        audioEngine.prepare()
        
        do {
            try audioEngine.start()
        } catch {
            print("audioEngine couldn't start because of an error.")
        }
    }
    
    func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
        if available {
            // microphoneButton.isEnabled = true
        } else {
            //   microphoneButton.isEnabled = false
        }
    }
    
    @objc func runTimedCode () {
         recognitionTask?.cancel()
        timer.invalidate()
        audioEngine.stop()
//        self.delegate?.recognitionFinished()
          self.navigationController?.popViewController(animated: true)
           self.delegate?.MicTypeSelected(text : self.lblText.text!)
           self.recognitionTask?.cancel()
    }

    
}
