function check(){
                if (mail_form.mail.value == ""){
                    //条件に一致する場合(メールアドレスが空の場合)
                    alert("URLを入力してください");    //エラーメッセージを出力
                    return false;    //送信ボタン本来の動作をキャンセルします
                }else{
                    //条件に一致しない場合(メールアドレスが入力されている場合)
                    return true;    //送信ボタン本来の動作を実行します
                }
            }