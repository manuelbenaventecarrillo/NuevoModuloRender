# Imagen base Odoo 17
FROM odoo:17

# (Opcional) módulos propios
COPY ./extra-addons /mnt/extra-addons

# Puerto HTTP de Odoo
EXPOSE 8069

# Puerto por defecto de PostgreSQL
ENV PGPORT=5432

# 1) Inicializa la BD indicada en $PGDATABASE si está vacía (stop-after-init)
# 2) Después arranca el servidor normalmente
#
# NOTA: usamos $PGDATABASE para que la inicialización vaya contra esa BD
# y --db-filter la fije para evitar que Odoo “coja” otra por error.
CMD ["bash","-lc", "\
  echo '==> Checking/initializing DB $PGDATABASE' && \
  odoo -d $PGDATABASE -i base --without-demo=all \
       --db_host=$PGHOST --db_port=$PGPORT \
       --db_user=$PGUSER --db_password=$PGPASSWORD \
       --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
       --stop-after-init || true; \
  echo '==> Starting Odoo server' && \
  odoo --db_host=$PGHOST --db_port=$PGPORT \
       --db_user=$PGUSER --db_password=$PGPASSWORD \
       --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
       --db-filter=$PGDATABASE \
       --http-port=${PORT}"]
