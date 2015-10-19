
(defun yaghurl-current-file ()
  "Copy yaghurl output to the clipboard for current file."
  (let* ((filename (buffer-file-name)))
    (call-process-shell-command (concat "yaghurl -o xclip " filename))))

(provide 'yaghurl)
