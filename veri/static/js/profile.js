
   $(document).ready(function () {
       $('.delete-file').on('click', function () {
           var fileId = $(this).data('file-id');
           deleteFile(fileId);
       });

       $('.download-file').on('click', function () {
        var fileUrl = $(this).data('file-url');

        // Dosyayı indirme işlemi
        fetch(fileUrl)
            .then(response => response.blob())
            .then(blob => {
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = fileUrl.split('/').pop(); // Dosya adını al
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => console.error('Dosya indirme hatası:', error));
    });

    

       function deleteFile(fileId) {
           var csrftoken = $('[name=csrfmiddlewaretoken]').val();

           $.ajax({
               url: `/delete_file/${fileId}/`,
               method: 'POST',
               headers: {'X-CSRFToken': csrftoken},
               success: function (data) {
                   if (data.status === 'success') {
                       // Başarıyla silindiğinde sayfayı yenile
                       location.reload();
                   } else {
                       alert('Dosya silinirken bir hata oluştu.');
                   }
               },
               error: function () {
                   alert('Dosya silinirken bir hata oluştu.');
               }
           });
       }
   });
